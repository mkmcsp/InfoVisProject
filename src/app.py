import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH
from dash import html, callback_context
import dash_bootstrap_components as dbc
import networkx as nx
from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.management.layout_mgt import layout_tab
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# how to use global variables
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
                    random_network('first-graph'),
                    dbc.Tabs(
                        layout_tab('first-layout-selection')
                    )
                ]),
            ], id='first-multiple', style={'height': '80vh'}),

            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col(circular_network('second-graph'), width=8),
                        dbc.Col(dbc.Tabs(layout_tab('second-layout-selection')))
                    ])
                ], id='second-multiple'),
                html.Div([
                    dbc.Row([
                        dbc.Col(spring_network('third-graph'), width=8),
                        dbc.Col(dbc.Tabs(layout_tab('third-layout-selection')))
                    ])
                ], id='third-multiple', style={'marginTop': '10px'})
            ], style={'marginRight': '20px'}),
        ]),
], style={'margin': '10px'})


@app.callback(
    Output('upload_data_modal', 'is_open'),
    Input('upload-data', 'n_clicks'),
)
def display_upload_modal(n_clicks):
    if n_clicks == 0:
        return
    return True


@app.callback(
    Output({'type': 'modal', 'index': MATCH}, 'is_open'),
    Input({'type': 'button', 'index': MATCH}, 'n_clicks'),
)
def display_modal(n_clicks):
    # basically if n_clicks = 0 it was not clicked before
    # very important to have this line or else the callback will be triggered whether the button was clicked or not
    if n_clicks == 0:
        return
    # prop_id = ast.literal_eval(callback_context.triggered[0]['prop_id'].split('.')[0])
    return True


@app.callback(
    Output('gene_selected', 'children'),
    Input('gene_selection', 'value'),
)
def display_modal(value):
    if value is None:
        return
    return dbc.Modal(dbc.ModalBody('You have selected {}'.format(value)), is_open=True)


if __name__ == '__main__':
    app.run_server(debug=True)
