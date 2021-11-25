import dash_bootstrap_components as dbc
from dash import html

table = dbc.Table([
    html.Tbody([
        html.Tr([html.Td('Temporary'), dbc.Input(value='Temporary', style={'border': None})]) for i in range(3)
    ])
], style={'marginTop': '10px'})


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
                        {'label': 'Cose (Compount Spring Embedder) layout', 'value': 'cose'},
                        {'label': 'Circular layout', 'value': 'circle'},
                        {'label': 'Concentric layout', 'value': 'concentric'},
                        {'label': 'Spectral layout', 'value': 'spectral'},
                        '''{'label': 'Cola layout', 'value': 'cola'},
                        {'label': 'Euler layout', 'value': 'euler'},
                        {'label': 'Spread layout', 'value': 'spread'},'''
                        # + layouts from networkx (graphviz)
                    ],
                    placeholder='Select a layout',
                    value='random'
                ),
                dbc.Row([
                    dbc.Col(table),
                    dbc.Col(table)
                ])

            ])
        )
    ], label='Layout', tab_id='layout_tab')
