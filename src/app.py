import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html
import dash_bootstrap_components as dbc
import networkx as nx
from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.management.layout_mgt import layout_tab
from layouts.body.graphs.utils import preprocess_data
import pandas as pd
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# how to use global variables ?
nodes = pd.read_csv('resources/genes.csv')
edges = pd.read_csv('resources/interactions.csv')

app.layout = html.Div([
    html.H1('InfoVis Project'),
    dbc.Row(
        [
            dbc.Col(management_column(nodes), width=2),
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
    dcc.Store(id='file_edges')
], style={'margin': '10px'})


@app.callback(
    [Output('upload_data_modal', 'is_open'),
     Output('dataset_elements', 'data'),
     Output({'type': 'layout-container', 'index': ALL}, 'children')],
    Input('upload-data', 'n_clicks'))
def display_upload_modal(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    file_nodes = 'nodes'
    file_edges = 'edges'
    elements = preprocess_data(file_nodes, file_edges, positions='random')
    return True, elements, [network(i+1, elements) for i in range(3)]


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
    Output({'type': 'layout-graph', 'index': ALL}, 'elements'),
    Input('gene_selection', 'value'),
    State('dataset_elements', 'data'))
def change_gene(value, elements):
    if value is None:
        raise PreventUpdate
    if 'overview' in value:
        return [elements for i in range(3)]

    #temporary
    gene_selected = '2'
    # select all matched edges first
    matched_edges = [element for element in elements if
                     'source' in element['data'] and gene_selected in element['data'].values()]
    list_nodes = set([edge['data'][x] for edge in matched_edges for x in ['source', 'target']])
    matched_nodes = [element for element in elements if
                     'id' in element['data'] and element['data']['id'] in list_nodes]
    return [matched_nodes + matched_edges for i in range(3)]


if __name__ == '__main__':
    app.run_server(debug=True)
