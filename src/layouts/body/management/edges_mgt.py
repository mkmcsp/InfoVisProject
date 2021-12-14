from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

colors_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(dbc.Input(type='color', value="#000000", id='colorpicker-edge',
                                  style={'width': 35, 'height': 25}), width=2),
                dbc.Col(dbc.Label(children=['#000000'], id='color-edge'), width=10)
            ]),
            dbc.Button('Apply', id='apply-edge-color', size='small', n_clicks_timestamp='0')
        ]
    ), style={'padding': '10px'}
)

sizes_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(dbc.Input(type='number', min=0.5, step=0.5, value=0.5, id='sizepicker-edge'), width=5),
            ]),
            dbc.Button('Apply', id='apply-edge-size', size='small', n_clicks_timestamp='0')
        ]
    ), style={'padding': '10px'}
)

edges_tab = dbc.Card(
    dbc.Tabs(
        [
            dbc.Tab(colors_content, id='edge-color-tab', label="Colors"),
            dbc.Tab(sizes_content, id='edge-size-tab', label="Size"),
        ], active_tab='edge-color-tab'
    )
)
