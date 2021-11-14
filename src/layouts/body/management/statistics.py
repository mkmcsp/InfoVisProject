from dash.dependencies import Input, Output, State, MATCH
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def list_stats():
    items = []
    for i in range(7):
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


stats_tab = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Metrics'),
            list_stats()
        ]
    )
)