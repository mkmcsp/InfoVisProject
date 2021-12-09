from dash.dependencies import Input, Output, State, MATCH
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def list_stats(nodes=None, edges=None):
    items = []
    items.append(dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P('Number of nodes')),
            dbc.Col(
                dbc.Button('Execute', size='sm', id={'type': 'button', 'index': 0}, n_clicks=0,
                           value='execute_n_nodes'),
                style={'text-align': 'right'}),
            dbc.Modal([dbc.ModalBody('Hello from nodes')],
                      id={'type': 'modal', 'index': 0}, is_open=False)
        ])
    ]))
    for i in range(1, 7):
        items.append(dbc.ListGroupItem([
            dbc.Row([
                dbc.Col(html.P('Community {}'.format(i)), id={'type': 'community', 'index': i}),
                dbc.Col(
                    dbc.Button('Execute', size='sm', id={'type': 'button', 'index': i}, n_clicks=0,
                               value='execute_{}'.format(i)),
                    style={'text-align': 'right'}),
                dbc.Modal([dbc.ModalBody('Hello from community {}'.format(i))],
                          id={'type': 'modal', 'index': i}, is_open=False)
            ])
        ]))

    return dbc.ListGroup(items, flush=True)


def summary(nodes, edges):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Summary'),
                list_stats()
            ]
        )
    )
