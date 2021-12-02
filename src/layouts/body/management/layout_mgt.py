import math
import datetime
import dash_bootstrap_components as dbc
from dash import html


def table_not_spring_shell():
    current = datetime.datetime.now()
    return html.Div([
        html.H4('Edit parameters'),
        dbc.Table([
            html.Tbody([
                html.Tr([html.Td('Scale', id=f"scale-{current}"), dbc.Input(type='number', min=1, value=1)])
            ])
        ]),
        dbc.Tooltip("Scale factor for positions.", target=f"scale-{current}", placement='top-start')
    ])


def table_shell():
    current = datetime.datetime.now()
    return html.Div([
        html.H4('Edit parameters'),
        dbc.Table([
            html.Tbody([
                html.Tr([html.Td('Rotate', id=f"rotate-{current}"), dbc.Input(type='number', value=1)])
            ])
        ]),
        dbc.Tooltip(
            "Angle (in radians) by which to rotate the starting position of each shell relative to the starting position of the previous shell.",
            target=f"rotate-{current}", placement='top-start')
    ])


def table_spring(n_nodes):
    current = datetime.datetime.now()
    return html.Div([
        html.H4('Edit parameters'),
        dbc.Table([
            html.Tbody([
                html.Tr([html.Td('Distance', id=f"distance-{current}"),
                         dbc.Input(type='number', value=(1 / math.sqrt(n_nodes)))]),
                html.Tr([html.Td('Number of iterations', id=f"iter-{current}"),
                         dbc.Input(type='number', min=1, value=50, step=1, )]),
                html.Tr([html.Td('Scale', id=f"scale-{current}"), dbc.Input(type='number', min=1, value=1)])
            ])
        ]),
        dbc.Tooltip("Optimal distance between nodes.", target=f"distance-{current}", placement='top-start'),
        dbc.Tooltip("Maximum number of iterations taken.", target=f"iter-{current}", placement='top-start'),
        dbc.Tooltip("Scale factor for positions.", target=f"scale-{current}", placement='top-start')
    ])


def layout_tab(index):
    return dbc.Tab([
        dbc.Card(
            dbc.CardBody([
                dbc.Select(
                    id={
                        'type': 'layout-selection',
                        'index': index
                    },
                    options=[
                        {'label': 'Fruchterman-Reingold layout', 'value': 'spring'},
                        {'label': 'Kamada-Kawai layout', 'value': 'kamadakawai'},
                        {'label': 'Spectral layout', 'value': 'spectral'},
                        {'label': 'Shell layout', 'value': 'shell'},
                        {'label': 'Circular layout', 'value': 'circular'},
                        {'label': 'Spiral layout', 'value': 'spiral'},
                        # + layouts from networkx (graphviz) ?
                    ],
                    placeholder='Select a layout',
                    value=[]
                ),
                dbc.Row([], id={'type': 'layout-management-div', 'index': index},
                        style={'marginTop': '10px', 'float': 'center'}),
                dbc.Button("Execute", id={'type': 'button-layout', 'index': index},
                           style={'float': 'right', 'marginTop': '10px'})
            ])
        )
    ], label='Layout', tab_id='layout_tab')
