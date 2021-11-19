from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

unique_colors = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Input(type='color', value="#000000", id='colorpicker-unique', style={'width': 35, 'height': 25}), width=2),
        dbc.Col(dbc.Label(children=['#000000'], id='color-unique'), width=10)
    ]),
    dbc.Button('Apply', id='apply-unique-color', size='small', n_clicks_timestamp='0')
], style={'padding': '10px'})

partition_colors = dbc.Card([
    dbc.Select(id='partition-select-color', placeholder='Select partition', options=[{'label': 'Temp', 'value': 'degree'}]),
    html.Div(id='partition-colors'),
    dbc.Button('Apply', id='apply-partition-colors', size='small', n_clicks_timestamp='0')
], style={'padding': '10px'})

colors_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Tabs([
                dbc.Tab(unique_colors, label='Unique'),
                dbc.Tab(partition_colors, label='Partition'),
                dbc.Tab(html.P(), label='Ranking'),
            ])
        ]
    )
)

unique_size = dbc.Card([
    dbc.Row([
        dbc.Col(dbc.Input(type='number', min=0.5, step=0.5, value=5, id='sizepicker-unique'), width=5),
    ]),
    dbc.Button('Apply', id='apply-unique-size', size='small', n_clicks_timestamp='0')
], style={'padding': '10px'})

ranking_size = dbc.Card([
    dbc.Select(id='ranking-select-size', placeholder='Select ranking', options=[{'label': 'Temp', 'value': 'degree'}]),
    html.Div(id='ranking-size'),
    html.Div(style={'display': 'none'}, id='ranking-labels'),
    dbc.Button('Apply', id='apply-ranking-size', size='small', n_clicks_timestamp='0')
], style={'padding': '10px'})

sizes_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Tabs([
                dbc.Tab(unique_size, label='Unique'),
                dbc.Tab(html.P('Mauvaise idée ?'), label='Partition'),
                dbc.Tab(ranking_size, label='Ranking'),
            ])
        ]
    )
)

nodes_tab = dbc.Card(
    dbc.Tabs(
        [
            dbc.Tab(colors_content, label="Colors"),
            dbc.Tab(sizes_content, label="Size"),
        ]
    )
)
