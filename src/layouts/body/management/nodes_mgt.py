from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# Add button instead of doing automatically
unique_colors = dbc.Card([
    dbc.Input(type='color', id='colorpicker-unique', style={'width': 35, 'height': 25})
], style={'padding': '10px'})

colors_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Tabs([
                dbc.Tab(unique_colors, label='Unique'),
                dbc.Tab(html.P(), label='Partition'),
                dbc.Tab(html.P(), label='Ranking'),
            ])
        ]
    )
)

sizes_content = dbc.Card(
    dbc.CardBody(
        [
            html.P('Temporary. What do I have to show here ?')
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
