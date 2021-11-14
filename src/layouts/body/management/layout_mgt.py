import dash_bootstrap_components as dbc
from dash import html

table = dbc.Table([
    html.Tbody([
        html.Tr([html.Td('Temporary'), dbc.Input(value='Temporary', style={'border': None})]) for i in range(3)
    ])
], style={'marginTop': '10px'})


def layout_tab(id):
    return dbc.Tab([
        dbc.Card(
            dbc.CardBody([
                dbc.Select(
                    id=id,
                    options=[
                        {'label': 'Fruchterman-Reingold layout', 'value': 'spring'},
                        {'label': 'Cose (Compount Spring Embedder) layout', 'value': 'cose'},
                        {'label': 'Circular layout', 'value': 'circular'},
                        {'label': 'Concentric layout', 'value': 'concentric'},
                        {'label': 'Cola layout', 'value': 'cola'},
                        {'label': 'Euler layout', 'value': 'euler'},
                        {'label': 'Spread layout', 'value': 'spread'},
                        # + layouts from networkx (graphviz)
                    ],
                    placeholder='Select a layout'
                ),
                dbc.Row([
                    dbc.Col(table),
                    dbc.Col(table)
                ])

            ])
        )
    ], label='Layout', tab_id='layout_tab')
