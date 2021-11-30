import dash_bootstrap_components as dbc
from dash import html

table_spectral = html.Div([
    html.H4('Edit parameters'),
    dbc.Table([
        html.Tbody([
            html.Tr([html.Td('Scale'), dbc.Input(type='number', min=1, value=1, style={'border': None})])
        ])
    ])
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
                        {'label': 'Spectral layout', 'value': 'spectral'},
                        {'label': 'Cose (Compount Spring Embedder) layout', 'value': 'cose'},
                        {'label': 'Circular layout', 'value': 'circle'},
                        {'label': 'Concentric layout', 'value': 'concentric'},
                        '''{'label': 'Cola layout', 'value': 'cola'},
                        {'label': 'Euler layout', 'value': 'euler'},
                        {'label': 'Spread layout', 'value': 'spread'},'''
                        # + layouts from networkx (graphviz) ?
                    ],
                    placeholder='Select a layout',
                    value='random'
                ),
                dbc.Row([], id={'type': 'layout-management-div', 'index': index},
                        style={'marginTop': '10px', 'float': 'center'}),
                dbc.Button("Execute", id={'type': 'button-layout', 'index': index},
                           style={'float': 'right', 'marginTop': '10px'})
            ])
        )
    ], label='Layout', tab_id='layout_tab')
