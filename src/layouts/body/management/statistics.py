from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc


def bar_chart(x, y, label):
    # return go.Figure(data=[go.Bar(x=x, y=y)])
    return px.scatter(x=x, y=y, labels={'x': label['x'], 'y': label['y']}, title="Degree Distribution")


def list_stats(nodes=None, edges=None, props=None):
    items = []
    items.append(dbc.ListGroupItem([
        html.P(f"Number of nodes : {len(nodes)}"),
        html.P(f"Number of edges : {len(edges)}")
    ]))
    items.append(dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P('Degree : ')),
            dbc.Col(
                dbc.Button('Execute', size='sm', id={'type': 'button-summary', 'index': 1}, n_clicks=0),
                style={'text-align': 'right'}),
            dbc.Modal([dbc.ModalBody([f"Average degree : {props['average_degree']:.2f}",
                                      html.Div(
                                          dcc.Graph(figure=bar_chart([i for i in range(len(props['degrees'][1]))],
                                                                  props['degrees'][1], {'x': 'Value', 'y': 'Count'}),
                                                    config={
                                                        'displaylogo': False,
                                                        'modeBarButtonsToRemove': ['sendDataToCloud', 'select2d', 'lasso2d']
                                                    })
                                      )])
                       ], id={'type': 'modal-summary', 'index': 1}, is_open=False, size='xl')
        ])
    ]))

    return dbc.ListGroup(items, flush=True)


def summary(nodes, edges, props):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Summary'),
                list_stats(nodes, edges, props)
            ]
        ), id='summary-component'
    )
