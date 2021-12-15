from layouts.body.management.management_component import management_column
from layouts.body.graphs.graphs import *
from layouts.body.graphs.management_graph import *
from layouts.body.management.informations_container import *


def body(nodes, edges, props):
    elements = nodes + edges
    return dbc.Row(
        [
            dbc.Col(
                management_column(nodes, edges, props), width=2),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Selected node', id='selected-card-header', color='secondary',
                                       style={'width': '412px',
                                              'borderRadius': 'calc(.4rem - 1px) calc(.4rem - 1px) 0 0'}),
                            dbc.Fade(
                                dbc.Card([
                                    dbc.CardBody(children=['No node has been selected.'], id='selected-node-card',
                                                 style={'width': 'inherit'}),
                                ], style={'width': '412px', 'maxHeight': '128px', 'overflowY': 'auto',
                                          'overflowX': 'hidden',
                                          'borderRadius': '0 0 calc(.4rem - 1px) calc(.4rem - 1px)'}),
                                id='fade-select-card', is_in=True
                            )
                        ]),
                        dbc.Col([
                            dbc.Button('Node on hover', id='hover-card-header', color='secondary',
                                       style={'width': '412px',
                                              'borderRadius': 'calc(.4rem - 1px) calc(.4rem - 1px) 0 0'}),
                            dbc.Fade(
                                dbc.Card([
                                    dbc.CardBody(children=['No node has been hovered.'], id='hover-node-card',
                                                 style={'width': 'inherit'}),
                                ], style={'width': '412px', 'maxHeight': '128px', 'overflowY': 'auto',
                                          'overflowX': 'hidden',
                                          'borderRadius': '0 0 calc(.4rem - 1px) calc(.4rem - 1px)'}),
                                id='fade-hover-card', is_in=True
                            ),
                        ])
                    ])
                ], style={'marginBottom': '20px', 'height': '105px'}),

                html.Div([
                    html.Div(network(1, elements), id={'type': 'layout-container', 'index': 1},
                             style={'height': '520px'}),
                    dbc.Tabs([
                        layout_tab(1),
                        edit_tab()
                    ], active_tab='layout_tab')
                ]),
            ], id='first-multiple', style={'height': '80vh'}),

            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(network(2, elements), id={'type': 'layout-container', 'index': 2}),
                                width=8),
                        dbc.Col(dbc.Tabs(layout_tab(2), active_tab='layout_tab'))
                    ])
                ], id='second-multiple'),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(network(3, elements), id={'type': 'layout-container', 'index': 3}),
                                width=8),
                        dbc.Col(dbc.Tabs(layout_tab(3), active_tab='layout_tab'))
                    ])
                ], id='third-multiple', style={'marginTop': '10px'})
            ]),
        ])
