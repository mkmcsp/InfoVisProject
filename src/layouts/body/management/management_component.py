from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from .filters import *
from .statistics import *
from .gene_selection import gene_selection
from .nodes_mgt import nodes_tab
from .edges_mgt import edges_tab


def tab(content, name, style=None):
    return dbc.Tab(content, label=name, style=style)


def upload_file_modal():
    select = dbc.Row([
        dbc.Label("Upload as a", html_for='type_upload', width=3),
        dbc.Col(
            dbc.Select(
                id='type_upload',
                options=[
                    {'label': 'list of nodes', 'value': 'list_nodes'},
                    {'label': 'list of edges', 'value': 'list_edges'},
                ],
                value='list_nodes',
                style={'margin': '5px'}
            )
        ),
    ], style={'textAlign': 'center'})
    upload = html.Div(
        dcc.Upload(dbc.Button('Choose file', n_clicks=0, color='secondary', style={'margin': '5px', 'width': '100%'})))
    submit = html.Div(dbc.Button("Submit", n_clicks=0, style={'marginTop': '10px', 'align': 'center'}))
    form = dbc.Form([select, upload, submit])
    output = dbc.Modal([
        dbc.ModalHeader('Upload your CSV file'),
        dbc.ModalBody(children=dbc.Form(form)),
    ], id='upload_data_modal', is_open=False, style={'textAlign': 'center'}, backdrop='static')
    return output


def management_column(nodes=None):
    return html.Div([
        # Upload file component
        html.Div([
            dbc.Button('Upload a CSV file', id='upload-data', n_clicks=0, style={
                'width': '100%',
                'height': '60px',
                'borderWidth': '1px',
                'textAlign': 'center',
                'margin': '0px 10px 10px 10px',
            }, ),
            upload_file_modal(),
        ]),

        dbc.Tabs(
            [
                tab(nodes_tab, "Nodes", {'marginLeft': '10px'}),
                tab(edges_tab, "Edges", {'marginLeft': '10px'})
            ], style={'marginLeft': '10px'}
        ),
        gene_selection(nodes),
        html.Div(id='gene_selected'),
        dbc.Tabs(
            [
                tab((list_filters()), "Filters", style={'marginLeft': '10px'}),
                tab(stats_tab, "Stats", style={'marginLeft': '10px'})
            ], style={'marginLeft': '10px', 'marginRight': '10px'}
        ),
    ])
