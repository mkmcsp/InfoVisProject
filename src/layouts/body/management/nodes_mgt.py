from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

unique_colors = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Input(type='color', value="#000000", id='colorpicker-unique', style={'width': 35, 'height': 25}),
                width=2),
        dbc.Col(dbc.Label(children=['#000000'], id='color-unique'), width=10)
    ]),
    dbc.Button('Apply', id='apply-unique-color', size='small')
], style={'padding': '10px'})

partition_colors = dbc.Card([
    dbc.Select(id='partition-select-color', placeholder='Select partition',
               options=[
                   {'label': 'Degree', 'value': 'degree'},
                   {'label': 'Community', 'value': 'community'},
                   {'label': 'Category', 'value': 'category'},
                   {'label': 'Subcategory', 'value': 'subcategory'},
                   {'label': 'Betweenness Centrality', 'value': 'betweenness'},
                   {'label': 'Closeness Centrality', 'value': 'closeness'},
                   {'label': 'Eigenvector Centrality', 'value': 'eigenvector'},
               ]),
    html.Div(id='partition-colors', style={'height': '150px', 'overflowY': 'auto', 'overflowX': 'hidden'}),
    dbc.Button('Apply', id='apply-partition-colors', size='small')
], style={'padding': '10px'})

ranking_colors = dbc.Card([
    dbc.Select(id='ranking-select-color', placeholder='Select partition',
               options=[
                   {'label': 'Degree', 'value': 'degree'},
                   {'label': 'Betweenness Centrality', 'value': 'brtweenness'},
                   {'label': 'Closeness Centrality', 'value': 'clrseness'},
                   {'label': 'Eigenvector Centrality', 'value': 'eirenvector'}
               ]),
    html.Div(id='ranking-colors'),
    html.Div(style={'display': 'none'}, id='ranking-color-labels'),
    dbc.Button('Apply', id='apply-ranking-colors', size='small')
], style={'padding': '10px'})

colors_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Tabs([
                dbc.Tab(unique_colors, tab_id='unique-node-color-tab', label='Unique'),
                dbc.Tab(partition_colors, tab_id='partition-node-color-tab', label='Partition'),
                dbc.Tab(ranking_colors, tab_id='ranking-node-color-tab', label='Ranking'),
            ], active_tab='unique-node-color-tab')
        ]
    )
)

unique_size = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Input(type='number', min=0.5, step=0.5, value=5, id='sizepicker-unique'), width=5),
    ]),
    dbc.Button('Apply', id='apply-unique-size', size='small')
], style={'padding': '10px'})

ranking_size = dbc.Card([
    dbc.Select(id='ranking-select-size', placeholder='Select ranking',
               options=[
                   {'label': 'Degree', 'value': 'degree'},
                   {'label': 'Betweenness centrality', 'value': 'brtweenness'},
                   {'label': 'Closeness Centrality', 'value': 'clrseness'},
                   {'label': 'Eigenvector Centrality', 'value': 'eirenvector'}
               ]),
    html.Div(id='ranking-size'),
    html.Div(style={'display': 'none'}, id='ranking-labels'),
    dbc.Button('Apply', id='apply-ranking-size', size='small')
], style={'padding': '10px'})

sizes_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Tabs([
                dbc.Tab(unique_size, tab_id='unique-node-size-tab', label='Unique'),
                dbc.Tab(ranking_size, tab_id='ranking-node-size-tab', label='Ranking'),
            ], active_tab='unique-node-size-tab')
        ]
    )
)

nodes_tab = html.Div(
    dbc.Tabs(
        [
            dbc.Tab(colors_content, tab_id='node-color-tab', label="Colors"),
            dbc.Tab(sizes_content, tab_id='node-size-tab', label="Size"),
        ], active_tab='node-color-tab'
    )
)
