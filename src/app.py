import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc
import networkx as nx
from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.management.layout_mgt import layout_tab
from layouts.body.management.edit_mgt import edit_tab
from layouts.body.graphs.utils import *
import pandas as pd
from dash.exceptions import PreventUpdate
import numpy as np
import copy

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

'''# how to use global variables ?
nodes = pd.read_csv('resources/genes.csv')
edges = pd.read_csv('resources/interactions.csv')'''

app.layout = html.Div([
    html.H1('InfoVis Project'),
    dbc.Row(
        [
            dbc.Col(management_column(), width=2),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader('Selected node'),
                                dbc.CardBody(children=['No node has been selected.'], id='selected-node-card')
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader('Node on hover'),
                                dbc.CardBody(id='hover-node-card')
                            ])
                        ])
                    ])
                ], style={'marginBottom': '10px', 'height': '105px'}),
                # should I put html.Div or dbc.Card ?
                html.Div([
                    html.Div(id={'type': 'layout-container', 'index': 1}, style={'height': '520px'}),
                    dbc.Tabs([
                        layout_tab(1),
                        edit_tab()
                    ])
                ]),
            ], id='first-multiple', style={'height': '80vh'}),

            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(id={'type': 'layout-container', 'index': 2}), width=8),
                        dbc.Col(dbc.Tabs(layout_tab(2)))
                    ])
                ], id='second-multiple'),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(id={'type': 'layout-container', 'index': 3}), width=8),
                        dbc.Col(dbc.Tabs(layout_tab(3)))
                    ])
                ], id='third-multiple', style={'marginTop': '10px'})
            ], style={'marginRight': '20px'}),
        ]),
    dcc.Store(id='dataset_elements'),
    dcc.Store(id='dataset_sub_elements'),
    dcc.Store(id='previous-selected-node', data=['None' for i in range(3)]),
    dcc.Store(id='previous-hover-node', data=['None' for i in range(3)]),
    dcc.Store(id='previous-gene-selection'),
    dcc.Store(id='default-stylesheet', data=default_stylesheet)
], style={'margin': '10px'})


@app.callback(
    [Output('upload_data_modal', 'is_open'),
     Output('dataset_elements', 'data'),
     Output('dataset_sub_elements', 'data'),
     Output({'type': 'layout-container', 'index': ALL}, 'children'),
     Output('gene_selection', 'options')],
    Input('upload-data', 'n_clicks'),
    State('gene_selection', 'options'))
def display_upload_modal(n_clicks, options):
    if n_clicks == 0:
        raise PreventUpdate
    file_nodes = pd.read_csv('resources/genes.csv')
    file_edges = pd.read_csv('resources/interactions.csv')
    nodes = pd.read_csv('resources/genes.csv')
    elements, sub_elements = preprocess_data(file_nodes, file_edges, positions='random')
    options.extend([{'label': node, 'value': node} for index, node in
                    nodes['OFFICIAL SYMBOL'].sort_values().iteritems()])
    return True, elements, sub_elements, [network(i + 1, sub_elements) for i in range(3)], options


@app.callback(
    Output({'type': 'modal', 'index': MATCH}, 'is_open'),
    Input({'type': 'button', 'index': MATCH}, 'n_clicks'),
)
def display_modal(n_clicks):
    # basically if n_clicks = 0 it was not clicked before
    # very important to have this line or else the callback will be triggered whether the button was clicked or not
    if n_clicks == 0:
        raise PreventUpdate
    # prop_id = ast.literal_eval(callback_context.triggered[0]['prop_id'].split('.')[0])
    return True


@app.callback(
    Output({'type': 'layout-graph', 'index': MATCH}, 'layout'),
    Input({'type': 'layout-selection', 'index': MATCH}, 'value'))
def change_layout(value):
    # temporary
    if value is None or 'spring' in value:
        raise PreventUpdate
    return {
        'name': value
    }


@app.callback(
    [Output({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
     Output('color-unique', 'children'),
     Output('color-edge', 'children'),
     Output('default-stylesheet', 'data')],
    [Input('apply-unique-color', 'n_clicks_timestamp'),
     Input('apply-partition-colors', 'n_clicks_timestamp'),
     Input('apply-unique-size', 'n_clicks_timestamp'),
     Input('apply-ranking-size', 'n_clicks_timestamp'),
     Input('apply-edge-color', 'n_clicks_timestamp'),
     Input('apply-edge-size', 'n_clicks_timestamp'),
     Input('toggle-label', 'value')],
    [State('colorpicker-unique', 'value'),
     State('default-stylesheet', 'data'),
     State({'type': 'colorpicker-partition', 'index': ALL}, 'value'),
     State('partition-select-color', 'value'),
     State({'type': 'colorlabel-partition', 'index': ALL}, 'children'),
     State('sizepicker-unique', 'value'),
     State({'type': 'sizepicker-ranking', 'index': ALL}, 'value'),
     State('ranking-select-size', 'value'),
     State('ranking-labels', 'children'),
     State('colorpicker-edge', 'value'),
     State('sizepicker-edge', 'value'),
     State({'type': 'layout-graph', 'index': ALL}, 'stylesheet')])
def change_stylesheet(n_clicks_unique_color, n_clicks_partition_color, n_clicks_unique_size, n_clicks_ranking_size,
                      n_clicks_ec, n_clicks_es, toggle_label, unique_value, actual_stylesheet, partition_values,
                      partition_type, partition_labels, unique_size, ranking_sizes, ranking_type, ranking_labels,
                      color_edge, size_edge, stylesheets):
    if len(stylesheets) == 0:
        raise PreventUpdate

    label_node = list(filter(lambda selector: selector['selector'] == 'node', actual_stylesheet))[0]
    if toggle_label:
        label_node['style']['content'] = 'data(label)'
    else:
        label_node['style']['content'] = ''

    if all(x == '0' for x in
           [n_clicks_unique_color, n_clicks_partition_color, n_clicks_ranking_size, n_clicks_unique_size, n_clicks_ec,
            n_clicks_es]):
        return [actual_stylesheet for i in range(3)], unique_value, color_edge, actual_stylesheet

    last_button_clicked = \
        sorted([int(n_clicks_unique_color)] + [int(n_clicks_partition_color)] + [int(n_clicks_ranking_size)] + [
            int(n_clicks_unique_size)] + [int(n_clicks_ec)] + [int(n_clicks_es)])[-1]

    if last_button_clicked == int(n_clicks_unique_color):
        new_style_node = list(filter(lambda selector: selector['selector'] == '.default', actual_stylesheet))[0]
        new_style_node['style']['background-color'] = unique_value

    elif last_button_clicked == int(n_clicks_partition_color):
        prefix = '.' + partition_type[:3]
        targeted_selectors = list(filter(lambda selector: prefix in selector['selector'], actual_stylesheet))
        # temporaire
        if len(targeted_selectors) == 0:
            for color_value, label in zip(partition_values, partition_labels):
                actual_stylesheet.append(
                    {'selector': prefix + str(label[0].split()[-1]), 'style': {'background-color': color_value}})
        else:
            for color_value, selector in zip(partition_values, targeted_selectors):
                selector['style']['background-color'] = color_value

    elif last_button_clicked == int(n_clicks_unique_size):
        new_style_node = list(filter(lambda selector: selector['selector'] == '.default', actual_stylesheet))[0]
        new_style_node['style']['height'] = unique_size
        new_style_node['style']['width'] = unique_size

    elif last_button_clicked == int(n_clicks_ranking_size):
        prefix = '.' + ranking_type[:3]
        targeted_selectors = list(filter(lambda selector: prefix in selector['selector'], actual_stylesheet))
        min = ranking_sizes[0]
        max = ranking_sizes[1]
        # temporaire
        if len(targeted_selectors) == 0:
            size_values = {label: size for label, size in
                           zip(ranking_labels, np.linspace(min, max, len(ranking_labels)))}
            for label, size in size_values.items():
                actual_stylesheet.append({'selector': '.' + label, 'style': {'height': size, 'width': size}})
        else:
            size_values = np.linspace(min, max, len(ranking_labels))
            for size_value, selector in zip(size_values, targeted_selectors):
                selector['style']['height'] = size_value
                selector['style']['width'] = size_value

    elif last_button_clicked == int(n_clicks_ec):
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['line-color'] = color_edge

    elif last_button_clicked == int(n_clicks_es):
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['width'] = size_edge

    # else:
    #    raise PreventUpdate

    # temporaire
    actual_stylesheet.append({
        'selector': '.selected',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }})
    actual_stylesheet.append({
        'selector': '.sub-selected',
        'style': {
            'background-color': 'red',
            'opacity': '0.2'
        }
    })
    return [actual_stylesheet for i in range(3)], unique_value, color_edge, actual_stylesheet


@app.callback(
    Output('partition-colors', 'children'),
    Input('partition-select-color', 'value'),
    State({'type': 'layout-graph', 'index': ALL}, 'elements'))  # elements will have the informations of partitions
def partition_colors(selection, elements):
    if selection is None:
        raise PreventUpdate
    elements = elements[0]
    # temporary
    selection = 'degree'
    prefix = selection[:3]
    partition_group = set()
    for element in elements:
        if 'classes' in element:
            partition_group.add([item for item in element['classes'].split() if item.startswith(prefix)][0])
        else:
            break
    return [dbc.Row([
        dbc.Col(dbc.Input(type='color', value="#000000", id={'type': 'colorpicker-partition', 'index': index},
                          style={'width': 35, 'height': 25}), width=2),
        dbc.Col(dbc.Label(children=[selection.capitalize() + ' ' + item[len(prefix):]],
                          id={'type': 'colorlabel-partition', 'index': index}), width=10)
    ]) for index, item in enumerate(list(sorted(partition_group)))]


@app.callback(
    [Output('ranking-size', 'children'),
     Output('ranking-labels', 'children')],
    Input('ranking-select-size', 'value'),
    State({'type': 'layout-graph', 'index': ALL}, 'elements'))  # elements will have the informations of partitions
def ranking_size(selection, elements):
    if selection is None:
        raise PreventUpdate
    elements = elements[0]
    # temporary
    selection = 'degree'
    prefix = selection[:3]
    ranking_group = set()
    for element in elements:
        if 'classes' in element:
            ranking_group.add([item for item in element['classes'].split() if item.startswith(prefix)][0])
        else:
            break
    return dbc.Row([
        dbc.Col([html.Span('Min'),
                 dbc.Input(type='number', min=0.5, step=0.5, id={'type': 'sizepicker-ranking', 'index': 1})], width=6),
        dbc.Col([html.Span('Max'),
                 dbc.Input(type='number', min=0.5, step=0.5, id={'type': 'sizepicker-ranking', 'index': 2})], width=6),
    ]), list(sorted(ranking_group))


@app.callback(
    [Output({'type': 'layout-graph', 'index': ALL}, 'elements'),
     Output('previous-selected-node', 'data'),
     Output('previous-hover-node', 'data'),
     Output('previous-gene-selection', 'data'),
     Output('selected-node-card', 'children'),
     Output('hover-node-card', 'children')],
    [Input('gene_selection', 'value'),
     Input({'type': 'layout-graph', 'index': ALL}, 'selectedNodeData'),
     Input({'type': 'layout-graph', 'index': ALL}, 'mouseoverNodeData')],
    [State('dataset_elements', 'data'),
     State('dataset_sub_elements', 'data'),
     State('previous-selected-node', 'data'),
     State('previous-hover-node', 'data'),
     State('previous-gene-selection', 'data'),
     State('selected-node-card', 'children'),
     State('hover-node-card', 'children')])
def change_gene(gene_selection_value, selected_nodes, hover_nodes, elements, sub_elements, previous_node_selected,
                previous_hover_node, previous_gene_selected, prev_selected_card, prev_hover_card):
    if gene_selection_value is None and all(node is None for node in selected_nodes) and all(
            node is None for node in hover_nodes):
        raise PreventUpdate

    # display gene selected
    if gene_selection_value is None or 'overview' in gene_selection_value:
        elements_to_return = sub_elements
    elif gene_selection_value is not None:
        # temporary
        gene_selected = gene_selection_value
        gene_selected_elements = match_node(gene_selected, elements)
        elements_to_return = gene_selected_elements

    # display selection of a node (interaction)
    if all(node is None or len(node) == 0 for node in selected_nodes) or len(selected_nodes) == 0 or (
            gene_selection_value is not None and previous_gene_selected != gene_selection_value):  # if the user has just selected a gene, we reset
        list_ids_to_return = ['None' for i in range(3)]
        selected_node_card = 'No node has been selected.'
    else:
        selected_nodes = [{'id': 'None'} if node is None or len(node) == 0 else node[0] for node in selected_nodes]
        list_ids = [node['id'] for node in selected_nodes]
        selected_node = [actual for (actual, previous) in zip(list_ids, previous_node_selected) if actual != previous]
        if len(selected_node) != 0:
            selected_node = selected_node[0]
            if selected_node != 'None':
                selected_node_card = str(selected_node)
                matched_selected_node = match_node(selected_node, elements_to_return)
                for element in elements_to_return:
                    data = element['data']
                    if element in matched_selected_node:
                        class_selection = 'sub-selected' if 'id' in data and data['id'] != selected_node else 'selected'
                    else:
                        class_selection = 'not-selected'

                    if 'classes' in element:
                        element['classes'] += ' ' + class_selection
                    else:
                        element['classes'] = class_selection
            else:
                list_ids = ['None' for i in range(3)]
                selected_node_card = 'No node has been selected.'
            list_ids_to_return = list_ids
        else:
            list_ids_to_return = previous_node_selected
            selected_node_card = 'No node has been selected.'

    # hover -> do i keep it ? Not sure
    if all(node is None or len(node) == 0 for node in hover_nodes) or len(hover_nodes) == 0 or (
            gene_selection_value is not None and previous_gene_selected != gene_selection_value):
        hover_ids_to_return = ['None' for i in range(3)]
        hovered_node_card = 'No node has been hovered.'
    else:
        hover_nodes = [{'id': 'None'} if node is None or len(node) == 0 else node for node in hover_nodes]
        list_ids = [node['id'] for node in hover_nodes]
        hovered_node = [actual for (actual, previous) in zip(list_ids, previous_hover_node) if actual != previous]
        if len(hovered_node) != 0:
            hovered_node = hovered_node[0]
            if hovered_node != 'None':
                hovered_node_card = str(hovered_node)
            else:
                list_ids = ['None' for i in range(3)]
                hovered_node_card = 'No node has been hovered.'
            hover_ids_to_return = list_ids
        else:
            hover_ids_to_return = previous_hover_node
            hovered_node_card = prev_hover_card

    return [elements_to_return for i in range(
        3)], list_ids_to_return, hover_ids_to_return, gene_selection_value, selected_node_card, hovered_node_card


if __name__ == '__main__':
    app.run_server(debug=True)
