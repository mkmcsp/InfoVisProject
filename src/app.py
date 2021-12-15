import ast
import json

import dash
from colour import Color
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc
import networkx as nx

from layouts.body.body import body
from layouts.body.graphs.graphs import *
from layouts.body.graphs.management_graph import *
from layouts.body.management.informations_container import *
from layouts.body.graphs.function_graphs import *
from layouts.body.script_process_file import process_file
from resources.stylesheet import default_stylesheet
import pandas as pd
from dash.exceptions import PreventUpdate
import numpy as np
import copy

app = dash.Dash(__name__, external_stylesheets=['assets/style.css', dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])
metrics_file = ['resources/communities.json', 'resources/betweenness.json', 'resources/closeness.json',
                'resources/eigenvector.json']
elements_nodes, elements_edges, props = preprocess_data(pd.read_csv('resources/genes.csv'),
                                                        pd.read_csv('resources/interactions.csv'), metrics_file)
elements_data = elements_nodes + elements_edges

app.layout = html.Div([
    html.H1("Caduceus"),
    html.H2("Gene interaction dashboard"),
    html.Div(children=body(elements_nodes, elements_edges, props), id='body'),

    ## Global variables
    dcc.Store(id='dataset_elements', data=elements_data),
    dcc.Store(id='props', data=props),
    dcc.Store(id='previous-hover-node', data=['None' for i in range(3)]),
    dcc.Store(id='previous-gene-selection'),
    dcc.Store(id='actual-stylesheet', data=default_stylesheet),
    dcc.Store(id='hightlight-color'),
    dcc.Store(id='previous-layout-selections', data=[[] for i in range(3)]),
    dcc.Store(id='layout-graphs'),
    dcc.Store(id='previous-elements-without-filter', data=elements_data)
], style={'margin': '10px', 'overflowY': 'auto', 'overflowX': 'hidden'})


@app.callback(
    [Output('body', 'children'),
     Output('props', 'data'),
     Output('dataset_elements', 'data')],
    [Input('submit-file', 'n_clicks'),
     Input('upload-data-nodes', 'contents'),
     Input('upload-data-edges', 'contents')])
def output_body(n_clicks, file_nodes, file_edges):
    if n_clicks == 0:
        raise PreventUpdate
    nodes_process, edges_process = process_file(file_nodes, file_edges)
    nodes, edges, properties = preprocess_data(nodes_process, edges_process)
    return body(nodes, edges, properties), properties, nodes + edges


@app.callback(
    Output('upload_data_modal', 'is_open'),
    Input('upload-data', 'n_clicks'))
def display_upload_modal(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    return True


@app.callback(
    Output({'type': 'modal-summary', 'index': MATCH}, 'is_open'),
    Input({'type': 'button-summary', 'index': MATCH}, 'n_clicks'),
)
def display_modal(n_clicks):
    # basically if n_clicks = 0 it was not clicked before
    # very important to have this line or else the callback will be triggered whether the button was clicked or not
    if n_clicks == 0:
        raise PreventUpdate
    return True


@app.callback(
    [Output('cat-filters', 'value'),
     Output('subcat-filters', 'value'),
     Output('degree-range', 'value'),
     Output('com-filters', 'value'),
     Output('bet-filters', 'value'),
     Output('clo-filters', 'value'),
     Output('eig-filters', 'value')],
    Input('reset-button', 'n_clicks'),
    [State('props', 'data')]
)
def reset_filters(n_clicks, properties):
    if n_clicks == 0:
        raise PreventUpdate
    deg = properties['degrees'][0]
    bet = properties['betweennesses'][0]
    clo = properties['closenesses'][0]
    eig = properties['eigenvectors'][0]
    return [], [], [deg[0], deg[-1]], [], [bet[0], bet[-1]], [clo[0], clo[-1]], [eig[0], eig[-1]]


@app.callback(
    [Output({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
     Output('color-unique', 'children'),
     Output('color-edge', 'children'),
     Output('actual-stylesheet', 'data')],
    [Input('apply-unique-color', 'n_clicks'),
     Input('apply-partition-colors', 'n_clicks'),
     Input('apply-unique-size', 'n_clicks'),
     Input('apply-ranking-size', 'n_clicks'),
     Input('apply-edge-color', 'n_clicks'),
     Input('apply-edge-size', 'n_clicks'),
     Input('apply-ranking-colors', 'n_clicks'),
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
     State('ranking-select-color', 'value'),
     State({'type': 'colorpicker-ranking', 'index': ALL}, 'value'),
     State('ranking-color-labels', 'children'),
     State('colorpicker-edge', 'value'),
     State('sizepicker-edge', 'value'),
     State({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
     State('hightlight-color', 'data')])
def change_stylesheet(n_clicks_unique_color, n_clicks_partition_color, n_clicks_unique_size, n_clicks_ranking_size,
                      n_clicks_ec, n_clicks_es, n_clicks_rc, toggle_label, highlight_color, unique_value,
                      actual_stylesheet, partition_values, partition_type, partition_labels, unique_size, ranking_sizes,
                      ranking_type, ranking_labels, ranking_type_color, ranking_color, ranking_color_labels, color_edge,
                      size_edge, stylesheets, hightlight_data):
    label_node = list(filter(lambda selector: selector['selector'] == 'node', actual_stylesheet))[0]

    ctx = dash.callback_context
    triggered = ctx.triggered
    if not triggered:
        raise PreventUpdate
    triggered = triggered[0]

    if 'toggle-label' in triggered['prop_id']:
        label_node['style']['content'] = 'data(id)' if toggle_label else ''

    if 'colorpicker-highlight' in triggered['prop_id']:
        if hightlight_data != highlight_color:
            actual_stylesheet.append({
                'selector': '.selected',
                'style': {
                    'background-color': highlight_color,
                    'line-color': highlight_color
                }})
            actual_stylesheet.append({
                'selector': '.demi-selected',
                'style': {
                    'background-color': highlight_color,
                    'opacity': '0.2'
                }
            })
        return [actual_stylesheet for i in range(3)], unique_value, color_edge, actual_stylesheet

    button_clicked = triggered['prop_id'].split('.')[0]

    if button_clicked == 'apply-unique-color':
        actual_stylesheet.append(
            {'selector': '.default', 'style': {'background-color': unique_value}})

    elif button_clicked == 'apply-partition-colors':
        prefix = '.' + partition_type[:3]

        for color_value, label in zip(partition_values, partition_labels):
            if prefix in ['.deg', '.com']:
                label = str(label[0].split()[-1])
            if prefix in ['.cat', '.sub']:
                label = label[0].replace(' ', '-').replace('/', '_')
            if prefix in ['.bet', '.clo', '.eig']:
                label = str(label[0]).replace('.', '_') if label[0] != 0 else '0_0'

            actual_stylesheet.append(
                {'selector': prefix + label, 'style': {'background-color': color_value}})

    elif button_clicked == 'apply-unique-size':
        actual_stylesheet.append(
            {'selector': '.default', 'style': {'height': unique_size, 'width': unique_size}})

    elif button_clicked == 'apply-ranking-size':
        prefix = ranking_type[:3]
        min = ranking_sizes[0]
        max = ranking_sizes[1]
        if prefix != 'deg':
            range_number = 11
            ranking_labels = list(set(map(lambda x: int(x * 10), ranking_labels)))
        else:
            range_number = int(ranking_labels[-1]) - int(ranking_labels[0]) + 1

        size_values = np.linspace(min, max, range_number)
        for label in ranking_labels:
            size = size_values[int(label)]
            actual_stylesheet.append(
                {'selector': '.{}{}'.format(prefix, int(label)), 'style': {'height': size, 'width': size}})

    elif button_clicked == 'apply-ranking-colors':
        prefix = ranking_type_color[:3]

        color = ranking_color[0]
        if prefix != 'deg':
            range_number = 11
            ranking_color_labels = list(set(map(lambda x: int(x * 10), ranking_color_labels)))
        else:
            range_number = int(ranking_color_labels[-1]) - int(ranking_color_labels[0]) + 1

        if 'viridis' in color:
            colors = list(Color("#eae51a").range_to(Color("#471063"), range_number))
        elif 'greyscale' in color:
            colors = list(Color("white").range_to(Color("black"), range_number))
        elif 'heat' in color:
            colors = list(Color("#fffdc3").range_to(Color("#ff2500"), range_number))
        elif 'yellow-green-blue' in color:
            colors = list(Color("#fcfed1").range_to(Color("#10236a"), range_number))
        for label in ranking_color_labels:
            color = colors[int(label)]
            actual_stylesheet.append(
                {'selector': '.{}{}'.format(prefix, int(label)), 'style': {'background-color': color.hex}})

    elif button_clicked == 'apply-edge-color':
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['line-color'] = color_edge

    elif button_clicked == 'apply-edge-size':
        new_style_node = list(filter(lambda selector: selector['selector'] == 'edge', actual_stylesheet))[0]
        new_style_node['style']['width'] = size_edge

    actual_stylesheet.append({
        'selector': '.selected',
        'style': {
            'background-color': highlight_color,
            'line-color': highlight_color
        }})
    actual_stylesheet.append({
        'selector': '.demi-selected',
        'style': {
            'background-color': highlight_color,
            'opacity': '0.2'
        }
    })

    return [actual_stylesheet for i in range(3)], unique_value, color_edge, actual_stylesheet


@app.callback(
    Output('partition-colors', 'children'),
    Input('partition-select-color', 'value'),
    [State('props', 'data')])
def partition_colors(selection, properties):
    if selection is None:
        raise PreventUpdate

    partition_group = set()

    if selection == 'category':
        partition_group = properties['categories'][0]
    elif selection == 'subcategory':
        partition_group = properties['subcategories'][0]
    elif selection == 'degree':
        partition_group = properties['degrees'][0]
    elif selection == 'community':
        partition_group = properties['communities'][0]
    elif selection == 'betweenness':
        partition_group = properties['betweennesses'][0]
    elif selection == 'closeness':
        partition_group = properties['closenesses'][0]
    elif selection == 'eigenvector':
        partition_group = properties['eigenvectors'][0]

    return [dbc.Row([
        dbc.Col(dbc.Input(type='color', value="#000000", id={'type': 'colorpicker-partition', 'index': index},
                          style={'width': 35, 'height': 25}), width=2),
        dbc.Col(dbc.Label(
            children=[selection.capitalize() + ' ' + str(item) if selection in ['degree', 'community'] else item],
            id={'type': 'colorlabel-partition', 'index': index}), width=10)
    ], style={'marginTop': '5px'}) for index, item in enumerate(partition_group)]


@app.callback(
    [Output('ranking-colors', 'children'),
     Output('ranking-color-labels', 'children')],
    Input('ranking-select-color', 'value'),
    [State('props', 'data')])
def ranking_color(selection, properties):
    if selection is None:
        raise PreventUpdate

    ranking_group = set()
    if selection == 'degree':
        ranking_group = properties['degrees'][0]
    if selection == 'brtweenness':
        ranking_group = properties['betweennesses'][0]
    if selection == 'clrseness':
        ranking_group = properties['closenesses'][0]
    if selection == 'eirenvector':
        ranking_group = properties['eigenvectors'][0]

    return dbc.Row([
        dbc.Col(html.Span('Colormap : ')),
        dbc.Col(dbc.Select(id={'type': 'colorpicker-ranking', 'index': 1}, value='viridis', options=[
            {'label': item.capitalize(), 'value': item} for item in
            ['viridis', 'greyscale', 'heat', 'yellow-green-blue']
        ])),
    ], style={'margin': '5px 0px 5px 0px'}), ranking_group


@app.callback(
    [Output('ranking-size', 'children'),
     Output('ranking-labels', 'children')],
    Input('ranking-select-size', 'value'),
    [State('props', 'data')])
def ranking_size(selection, properties):
    if selection is None:
        raise PreventUpdate

    ranking_group = set()
    if selection == 'degree':
        ranking_group = properties['degrees'][0]
    if selection == 'brtweenness':
        ranking_group = properties['betweennesses'][0]
    if selection == 'clrseness':
        ranking_group = properties['closenesses'][0]
    if selection == 'eirenvector':
        ranking_group = properties['eigenvectors'][0]

    return dbc.Row([
        dbc.Col([html.Span('Min'),
                 dbc.Input(type='number', min=0.5, step=0.5, id={'type': 'sizepicker-ranking', 'index': 1})], width=6),
        dbc.Col([html.Span('Max'),
                 dbc.Input(type='number', min=0.5, step=0.5, id={'type': 'sizepicker-ranking', 'index': 2})], width=6),
    ], style={'margin': '5px 0px 5px 0px'}), ranking_group


@app.callback(
    Output('fade-hover-card', 'is_in'),
    Input('hover-card-header', 'n_clicks'),
    State('fade-hover-card', 'is_in'))
def toggle_card_hover(n_clicks, is_in):
    if n_clicks is None:
        raise PreventUpdate
    return not is_in


@app.callback(
    Output('fade-select-card', 'is_in'),
    Input('selected-card-header', 'n_clicks'),
    State('fade-select-card', 'is_in'))
def toggle_card_select(n_clicks, is_in):
    if n_clicks is None:
        raise PreventUpdate
    return not is_in


@app.callback(
    Output('selected-card-header', 'children'),
    Input({'type': 'layout-graph', 'index': ALL}, 'selectedNodeData'))
def change_header_card_select(selection):
    ctx = dash.callback_context
    triggered = ctx.triggered

    if not triggered or len(triggered[0]['value']) != 2:
        return 'Selected node'
    source, target = triggered[0]['value']
    return f"Shortest path between {source['id']} and {target['id']}"


@app.callback(
    Output('hover-node-card', 'children'),
    Input({'type': 'layout-graph', 'index': ALL}, 'mouseoverNodeData'),
    State({'type': 'layout-graph', 'index': ALL}, 'elements'))
def hover_node(hover_nodes, elements):
    ctx = dash.callback_context
    triggered = ctx.triggered

    if not triggered:
        return 'No node has been hovered.'

    hovered_node = triggered[0]['value']['id']
    return node_info([elt for elt in elements[0] if 'id' in elt['data'] and hovered_node == elt['data']['id']][0])


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
        elif layout_algorithm is None or len(layout_algorithm) == 0:
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
     Output('layout-graphs', 'data'),
     Output('previous-elements-without-filter', 'data')],
    [Input({'type': 'layout-selection', 'index': ALL}, 'value'),
     Input('gene_selection', 'value'),
     Input({'type': 'layout-graph', 'index': ALL}, 'selectedNodeData'),
     Input({'type': 'button-layout', 'index': ALL}, 'n_clicks'),
     Input('filter-button', 'n_clicks')],
    [State('dataset_elements', 'data'),
     State('layout-graphs', 'data'),
     State('previous-gene-selection', 'data'),
     State({'type': 'layout-management-div', 'index': ALL}, 'children'),
     State('previous-elements-without-filter', 'data'),
     State('cat-filters', 'value'),
     State('subcat-filters', 'value'),
     State('degree-range', 'value'),
     State('com-filters', 'value'),
     State('bet-filters', 'value'),
     State('clo-filters', 'value'),
     State('eig-filters', 'value'),
     State('props', 'data')])
def change_gene(layout_selections, gene_selection_value, selected_nodes, btn_click, filter_btn, elements,
                elts_layout, previous_gene_selected, layout_divs, previous_elements_without_filter, cat_choice,
                subcat_choice, degree_range, com_choice, bet_range, clo_range, eig_range, properties):
    ctx = dash.callback_context
    triggered = ctx.triggered

    if all(len(layout) == 0 for layout in layout_selections) and gene_selection_value is None and not triggered:
        raise PreventUpdate

    triggered = triggered[0]
    elements_without_filter = previous_elements_without_filter

    # display gene selected
    if gene_selection_value is None or 'overview' in gene_selection_value:
        if gene_selection_value == previous_gene_selected:
            if elts_layout is None:
                elts_layout = [elements for i in range(3)]
            elements_to_return = elts_layout
        else:
            layout_selections = [[] for i in range(3)]
            elements_to_return = [elements for i in range(3)]
            elements_without_filter = copy.deepcopy(elements_to_return[0])

    elif gene_selection_value is not None:
        gene_selected = gene_selection_value
        if all(layout is None for layout in layout_selections) or gene_selected != previous_gene_selected:
            gene_selected_elements = match_node_all_data(gene_selected, elements)
            elements_to_return = [gene_selected_elements for i in range(3)]
            layout_selections = [[] for i in range(3)]
            elements_without_filter = copy.deepcopy(elements_to_return[0])
        else:
            elements_to_return = elts_layout

    # display layout selection
    if 'button-layout' not in triggered['prop_id']:
        layout_selections_return = layout_selections
    else:
        index_changed = json.loads(triggered['prop_id'][:-9])['index'] - 1
        new_layout = layout_selections[index_changed]
        html_components = layout_divs[index_changed]['props']['children'][1]['props']['children'][0]['props'][
            'children']
        params = [component['props']['children'][1]['props']['value'] for component in html_components]
        elements_changed = change_layout(elements_to_return[index_changed], new_layout, params=params)
        elements_to_return = [element if index != index_changed else elements_changed for index, element in
                              enumerate(elements_to_return)]
        layout_selections_return = layout_selections

    # display filter
    if 'filter-button' in triggered['prop_id']:
        cat_choice = cat_choice if len(cat_choice) != 0 else properties['categories'][0]
        subcat_choice = subcat_choice if len(subcat_choice) != 0 else properties['subcategories'][0]
        com_choice = com_choice if len(com_choice) != 0 else properties['communities'][0]
        elements_to_return = [filter_nodes(elts_layout[i], copy.deepcopy(elements_without_filter),
                                           {'degree': degree_range, 'categories': cat_choice,
                                            'subcategories': subcat_choice, 'communities': com_choice,
                                            'betweenness': bet_range, 'closeness': clo_range, 'eigenvector': eig_range})
                              for i in range(3)]

    layout_graphs = copy.deepcopy(elements_to_return)

    # display selection of a node (interaction)
    if 'selectedNodeData' in triggered['prop_id']:
        if len(triggered['value']) == 0 or len(triggered['value']) > 2:
            selected_node_card = 'No node has been selected.'
        else:
            elements_details = elements_to_return[0]
            if len(triggered['value']) == 1:
                selected_node = triggered['value'][0]['id']
                nodes_highlighted, edges_highlighted = match_node_only_id(selected_node, elements_details)
                node_element = get_node_info(selected_node, elements_details)
                selected_node_card = node_info(node_element)

            elif len(triggered['value']) == 2:
                source, target = map(lambda x: x['id'], triggered['value'])
                nodes_highlighted, edges_highlighted, info, path = get_shortest_path_from_to(elements_details, source,
                                                                                             target)
                if nodes_highlighted is None:
                    selected_node_card = f"No path between {source} and {target}."
                    selected_node = None
                else:
                    selected_node = nodes_highlighted
                    selected_node_card = path_info(info, path)

            for elt1, elt2, elt3 in zip(elements_to_return[0], elements_to_return[1], elements_to_return[2]):
                data = elt1['data']
                if selected_node is not None and (('id' in data and data['id'] in nodes_highlighted) or (
                        'source' in data and (((data['source'], data['target']) in edges_highlighted) or
                                              ((data['target'], data['source']) in edges_highlighted)))):
                    class_selection = 'demi-selected' if 'source' not in data and data[
                        'id'] not in selected_node else 'selected'
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
    else:
        selected_node_card = 'No node has been selected.'

    return elements_to_return, gene_selection_value, selected_node_card, layout_selections_return, layout_selections_return, layout_graphs, elements_without_filter


if __name__ == '__main__':
    app.run_server(debug=True)
