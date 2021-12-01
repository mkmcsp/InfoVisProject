import json

import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc
import networkx as nx
from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.management.layout_mgt import *
from layouts.body.management.edit_mgt import edit_tab
from layouts.body.graphs.utils import *
import pandas as pd
from dash.exceptions import PreventUpdate
import numpy as np
import copy

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
elements_data = preprocess_data(pd.read_csv('resources/genes.csv'), pd.read_csv('resources/interactions.csv'), 'sub')

app.layout = html.Div([
    html.H1('InfoVis Project'),
    dbc.Row(
        [
            dbc.Col(management_column(pd.read_csv('resources/genes.csv')), width=2),
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
                    html.Div(network(1, elements_data), id={'type': 'layout-container', 'index': 1},
                             style={'height': '520px'}),
                    dbc.Tabs([
                        layout_tab(1),
                        edit_tab()
                    ])
                ]),
            ], id='first-multiple', style={'height': '80vh'}),

            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(network(2, elements_data), id={'type': 'layout-container', 'index': 2}),
                                width=8),
                        dbc.Col(dbc.Tabs(layout_tab(2)))
                    ])
                ], id='second-multiple'),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(network(3, elements_data), id={'type': 'layout-container', 'index': 3}),
                                width=8),
                        dbc.Col(dbc.Tabs(layout_tab(3)))
                    ])
                ], id='third-multiple', style={'marginTop': '10px'})
            ], style={'marginRight': '20px'}),
        ]),
    dcc.Store(id='dataset_elements',
              data=preprocess_data(pd.read_csv('resources/genes.csv'), pd.read_csv('resources/interactions.csv'))),
    dcc.Store(id='dataset_sub_elements',
              data=preprocess_data(pd.read_csv('resources/genes.csv'), pd.read_csv('resources/interactions.csv'),
                                   'sub')),
    dcc.Store(id='previous-hover-node', data=['None' for i in range(3)]),
    dcc.Store(id='previous-gene-selection'),
    dcc.Store(id='actual-stylesheet', data=default_stylesheet),
    dcc.Store(id='hightlight-color'),
    dcc.Store(id='previous-layout-selections', data=['random' for i in range(3)]),
    dcc.Store(id='layout-graphs')
], style={'margin': '10px'})


@app.callback(
    [Output('upload_data_modal', 'is_open'),
     Output('dataset_elements', 'data'),
     Output({'type': 'layout-container', 'index': ALL}, 'children'),
     Output('gene_selection', 'options')],
    Input('upload-data', 'n_clicks'),
    State('gene_selection', 'options'))
def display_upload_modal(n_clicks, options):
    if n_clicks == 0:
        raise PreventUpdate


'''    file_nodes = pd.read_csv('resources/genes.csv')
    file_edges = pd.read_csv('resources/interactions.csv')
    elements, sub_elements = preprocess_data(file_nodes, file_edges, positions='random')
    options.extend([{'label': node, 'value': node} for index, node in
                    file_nodes['OFFICIAL SYMBOL'].sort_values().iteritems()])
    return True, elements, sub_elements, [network(i + 1, sub_elements) for i in range(3)], options'''


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
    [Output({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
     Output('color-unique', 'children'),
     Output('color-edge', 'children'),
     Output('actual-stylesheet', 'data')],
    [Input('apply-unique-color', 'n_clicks_timestamp'),
     Input('apply-partition-colors', 'n_clicks_timestamp'),
     Input('apply-unique-size', 'n_clicks_timestamp'),
     Input('apply-ranking-size', 'n_clicks_timestamp'),
     Input('apply-edge-color', 'n_clicks_timestamp'),
     Input('apply-edge-size', 'n_clicks_timestamp'),
     Input('toggle-label', 'value'),
     Input('colorpicker-highlight', 'value')],
    [State('colorpicker-unique', 'value'),
     State('actual-stylesheet', 'data'),
     State({'type': 'colorpicker-partition', 'index': ALL}, 'value'),
     State('partition-select-color', 'value'),
     State({'type': 'colorlabel-partition', 'index': ALL}, 'children'),
     State('sizepicker-unique', 'value'),
     State({'type': 'sizepicker-ranking', 'index': ALL}, 'value'),
     State('ranking-select-size', 'value'),
     State('ranking-labels', 'children'),
     State('colorpicker-edge', 'value'),
     State('sizepicker-edge', 'value'),
     State({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
     State('hightlight-color', 'data')])
def change_stylesheet(n_clicks_unique_color, n_clicks_partition_color, n_clicks_unique_size, n_clicks_ranking_size,
                      n_clicks_ec, n_clicks_es, toggle_label, highlight_color, unique_value, actual_stylesheet,
                      partition_values, partition_type, partition_labels, unique_size, ranking_sizes, ranking_type,
                      ranking_labels, color_edge, size_edge, stylesheets, hightlight_data):
    label_node = list(filter(lambda selector: selector['selector'] == 'node', actual_stylesheet))[0]
    if toggle_label:
        label_node['style']['content'] = 'data(label)'
    else:
        label_node['style']['content'] = ''

    if all(x == '0' for x in
           [n_clicks_unique_color, n_clicks_partition_color, n_clicks_ranking_size, n_clicks_unique_size, n_clicks_ec,
            n_clicks_es]):
        if hightlight_data != highlight_color:
            actual_stylesheet.append({
                'selector': '.selected',
                'style': {
                    'background-color': highlight_color,
                    'line-color': highlight_color
                }})
            actual_stylesheet.append({
                'selector': '.sub-selected',
                'style': {
                    'background-color': highlight_color,
                    'opacity': '0.2'
                }
            })
        return [actual_stylesheet for i in range(3)], unique_value, color_edge, actual_stylesheet

    last_button_clicked = \
        sorted([int(n_clicks_unique_color)] + [int(n_clicks_partition_color)] + [int(n_clicks_ranking_size)] + [
            int(n_clicks_unique_size)] + [int(n_clicks_ec)] + [int(n_clicks_es)])[-1]

    if last_button_clicked == int(n_clicks_unique_color):
        actual_stylesheet.append(
            {'selector': '.default', 'style': {'background-color': unique_value}})

    elif last_button_clicked == int(n_clicks_partition_color):
        prefix = '.' + partition_type[:3]
        for color_value, label in zip(partition_values, partition_labels):
            actual_stylesheet.append(
                {'selector': prefix + str(label[0].split()[-1]), 'style': {'background-color': color_value}})

    elif last_button_clicked == int(n_clicks_unique_size):
        actual_stylesheet.append(
            {'selector': '.default', 'style': {'height': unique_size, 'width': unique_size}})

    elif last_button_clicked == int(n_clicks_ranking_size):
        min = ranking_sizes[0]
        max = ranking_sizes[1]
        size_values = np.linspace(min, max, int(ranking_labels[-1][3:]) - int(ranking_labels[0][3:]) + 1)
        for label in ranking_labels:
            size = size_values[int(label[3:]) - 1]
            actual_stylesheet.append({'selector': '.' + label, 'style': {'height': size, 'width': size}})

    elif last_button_clicked == int(n_clicks_ec):
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['line-color'] = color_edge

    elif last_button_clicked == int(n_clicks_es):
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['width'] = size_edge

    else:
        raise PreventUpdate

    actual_stylesheet.append({
        'selector': '.selected',
        'style': {
            'background-color': highlight_color,
            'line-color': highlight_color
        }})
    actual_stylesheet.append({
        'selector': '.sub-selected',
        'style': {
            'background-color': highlight_color,
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
    Output('hover-node-card', 'children'),
    Output('previous-hover-node', 'data'),
    Input({'type': 'layout-graph', 'index': ALL}, 'mouseoverNodeData'),
    State('previous-hover-node', 'data'),
    State('hover-node-card', 'children'))
def hover_node(hover_nodes, previous_hover_node, prev_hover_card):
    if all(node is None or len(node) == 0 for node in hover_nodes) or len(hover_nodes) == 0:
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
    return hovered_node_card, hover_ids_to_return


@app.callback(
    Output({'type': 'layout-management-div', 'index': MATCH}, 'children'),
    [Input({'type': 'layout-selection', 'index': MATCH}, 'value'),
     Input({'type': 'button-layout', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'layout-management-div', 'index': MATCH}, 'children'),
     State({'type': 'layout-graph', 'index': MATCH}, 'elements')])
def change_table_layout(layout_algorithm, n_clicks, div, elements):
    if layout_algorithm is None:
        raise PreventUpdate
    ctx = dash.callback_context
    triggered = ctx.triggered[0]

    if 'button-layout' in triggered['prop_id']:
        return div
    else:
        if 'spring' in layout_algorithm:
            return table_spring(len([data for data in elements if 'source' not in data['data']]))
        elif layout_algorithm is None:
            return []
        elif 'shell' in layout_algorithm:
            return table_shell()
        else:
            return table_not_spring_shell()


@app.callback(
    [Output({'type': 'layout-graph', 'index': ALL}, 'elements'),
     Output('previous-gene-selection', 'data'),
     Output('selected-node-card', 'children'),
     Output('previous-layout-selections', 'data'),
     Output({'type': 'layout-selection', 'index': ALL}, 'value'),
     Output('layout-graphs', 'data')],
    [Input({'type': 'layout-selection', 'index': ALL}, 'value'),
     Input('gene_selection', 'value'),
     Input({'type': 'layout-graph', 'index': ALL}, 'selectedNodeData'),
     Input({'type': 'button-layout', 'index': ALL}, 'n_clicks')],
    [State('dataset_elements', 'data'),
     State('layout-graphs', 'data'),
     State('dataset_sub_elements', 'data'),
     State('previous-layout-selections', 'data'),
     State('previous-gene-selection', 'data'),
     State({'type': 'layout-management-div', 'index': ALL}, 'children')])
def change_gene(layout_selections, gene_selection_value, selected_nodes, btn_click, elements, elts_layout, sub_elements,
                prev_layout_sel, previous_gene_selected, layout_divs):
    ctx = dash.callback_context
    triggered = ctx.triggered

    if all(layout is None for layout in layout_selections) and gene_selection_value is None and not triggered:
        raise PreventUpdate

    triggered = triggered[0]

    # display gene selected
    if gene_selection_value is None or 'overview' in gene_selection_value:
        if gene_selection_value != previous_gene_selected:
            layout_selections = [None for i in range(3)]
        elements_to_return = [sub_elements for i in range(3)]
    elif gene_selection_value is not None:
        gene_selected = gene_selection_value
        if all(layout is None for layout in layout_selections) or gene_selected != previous_gene_selected:
            gene_selected_elements = match_node_all_data(gene_selected, elements)
            elements_to_return = [gene_selected_elements for i in range(3)]
            layout_selections = [None for i in range(3)]
        else:
            elements_to_return = [match_node_all_data(gene_selected, elts_layout[0]),
                                  match_node_all_data(gene_selected, elts_layout[1]),
                                  match_node_all_data(gene_selected, elts_layout[2])]

    # display layout selection
    if 'button-layout' not in triggered['prop_id']:
        layout_selections_return = layout_selections
    else:
        index_changed = json.loads(triggered['prop_id'][:-9])['index'] - 1
        new_layout = layout_selections[index_changed]
        html_components = layout_divs[index_changed]['props']['children'][1]['props']['children'][0]['props'][
            'children']
        params = [component['props']['children'][1]['props']['value'] for component in html_components]

        if elts_layout is None:
            elts_layout = copy.deepcopy(elements_to_return)

        elements_changed = change_layout(elts_layout[index_changed], new_layout, params=params)
        elements_to_return = [element if index != index_changed else elements_changed for index, element in
                              enumerate(elts_layout)]
        layout_selections_return = layout_selections
    layout_graphs = copy.deepcopy(elements_to_return)

    # display selection of a node (interaction)
    if 'selectedNodeData' in triggered['prop_id']:
        if len(triggered['value']) == 0:
            selected_node_card = 'No node has been selected.'
        else:
            selected_node = triggered['value'][0]['id']
            selected_node_card = selected_node
            elts_temps = elements_to_return[0]
            matched_selected_node, matched_selected_edge = match_node_only_id(selected_node, elts_temps)
            for elt1, elt2, elt3 in zip(elements_to_return[0], elements_to_return[1], elements_to_return[2]):
                data = elt1['data']
                if ('id' in data and data['id'] in matched_selected_node) or (
                        'source' in data and (data['source'], data['target']) in matched_selected_edge):
                    class_selection = 'sub-selected' if 'id' in data and data['id'] != selected_node else 'selected'
                else:
                    class_selection = 'not-selected'
                if 'classes' in elt1:
                    elt1['classes'] += ' ' + class_selection
                    elt2['classes'] += ' ' + class_selection
                    elt3['classes'] += ' ' + class_selection
                else:
                    elt1['classes'] = class_selection
                    elt2['classes'] = class_selection
                    elt3['classes'] = class_selection

            elements_to_return = elements_to_return
    else:
        selected_node_card = 'No node has been selected.'

    return elements_to_return, gene_selection_value, selected_node_card, layout_selections_return, layout_selections_return, layout_graphs


if __name__ == '__main__':
    app.run_server(debug=True)
