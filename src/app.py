import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc
import networkx as nx
from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.management.layout_mgt import layout_tab
from layouts.body.graphs.utils import *
import pandas as pd
from dash.exceptions import PreventUpdate

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
                dbc.ButtonGroup([
                    dbc.Button("First"),
                    dbc.Button("Second"),
                    dbc.Button("Third"),
                ], style={'marginBottom': '10px'}),
                # should I put html.Div or dbc.Card ?
                html.Div([
                    html.Div(id={'type': 'layout-container', 'index': 1}, style={'height': '520px'}),
                    dbc.Tabs(
                        layout_tab(1)
                    )
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
    dcc.Store(id='previous-selected-node', data=['None' for i in range(3)]),
    dcc.Store(id='previous-gene-selection')
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
    file_nodes = 'nodes'
    file_edges = 'edges'
    nodes = pd.read_csv('resources/genes.csv')
    elements = preprocess_data(file_nodes, file_edges, positions='random')
    options.extend([{'label': node, 'value': node} for index, node in
                    nodes['OFFICIAL SYMBOL'].sort_values().iteritems()])
    return True, elements, [network(i + 1, elements) for i in range(3)], options


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
    if value is None or 'spring' in value: return
    return {
        'name': value
    }


@app.callback(
    Output({'type': 'layout-graph', 'index': ALL}, 'stylesheet'),
    Input('colorpicker-unique', 'value'),
    State({'type': 'layout-graph', 'index': ALL}, 'stylesheet'))
def change_stylesheet(value, actual_stylesheet):
    actual_stylesheet = actual_stylesheet[0]
    if value is None:
        raise PreventUpdate
    new_style_node = list(filter(lambda selector: selector['selector'] == '.default', actual_stylesheet))[0]
    new_style_node['style']['background-color'] = value
    st = next(item for item in actual_stylesheet if item['selector'] == '.default')
    st.update(new_style_node)
    return [actual_stylesheet for i in range(3)]


@app.callback(
    [Output({'type': 'layout-graph', 'index': ALL}, 'elements'),
     Output('previous-selected-node', 'data'),
     Output('previous-gene-selection', 'data')],
    [Input('gene_selection', 'value'),
     Input({'type': 'layout-graph', 'index': ALL}, 'selectedNodeData')],
    [State('dataset_elements', 'data'),
     State('previous-selected-node', 'data'),
     State('previous-gene-selection', 'data')])
def change_gene(gene_selection_value, selected_nodes, elements, previous_node_selected, previous_gene_selected):
    if gene_selection_value is None and all(node is None for node in selected_nodes):
        raise PreventUpdate

    # display gene selected
    if gene_selection_value is None or 'overview' in gene_selection_value:
        elements_to_return = elements
    elif gene_selection_value is not None:
        # temporary
        gene_selected = '2'
        gene_selected_elements = match_node(gene_selected, elements)
        elements_to_return = gene_selected_elements

    # display selection of a node (interaction)
    if all(node is None or len(node) == 0 for node in selected_nodes) or len(selected_nodes) == 0 or (
            gene_selection_value is not None and previous_gene_selected != gene_selection_value):  # if the user has just selected a gene, we reset
        list_ids_to_return = ['None' for i in range(3)]
        for element in elements_to_return:
            element['classes'] = 'default'
    else:
        selected_nodes = [[{'id': 'None'}] if node is None or len(node) == 0 else node for node in selected_nodes]
        list_ids = [dico['id'] for node in selected_nodes for dico in node]
        selected_node = [actual for (actual, previous) in zip(list_ids, previous_node_selected) if actual != previous][
            0]
        if selected_node != 'None':
            matched_selected_node = match_node(selected_node, elements_to_return)
            for element in elements_to_return:
                data = element['data']
                if element in matched_selected_node:
                    element['classes'] = 'sub-selected' if 'id' in data and data['id'] != selected_node else 'selected'
                else:
                    element['classes'] = 'not-selected'
        else:
            list_ids = ['None' for i in range(3)]
            for element in elements_to_return:
                element['classes'] = 'default'

        list_ids_to_return = list_ids
    return [elements_to_return for i in range(3)], list_ids_to_return, gene_selection_value


if __name__ == '__main__':
    app.run_server(debug=True)
