from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
import math


def scatter_plot(x, y, label, title):
    return px.scatter(x=x, y=y, labels={'x': label['x'], 'y': label['y']}, title=title)


def bar_chart(x, y, label, title):
    fig = px.bar(x=x, y=y, labels={'x': label['x'], 'y': label['y']}, title=title)
    fig = fig.update_layout(yaxis_range=[0, math.ceil(9108 / 1000.0) * 1000.0])
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    return fig


def list_stats(nodes_length=None, edges=None, props=None):
    config_modal = {'displaylogo': False, 'modeBarButtonsToRemove': ['sendDataToCloud', 'select2d', 'lasso2d']}
    items = []
    items.append(dbc.ListGroupItem([
        html.P(f"Number of nodes : {nodes_length}"),
        html.P(f"Number of edges : {len(edges)}")
    ]))
    items.append(dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P('Degree : ')),
            dbc.Col(
                dbc.Button('Show', size='sm', id={'type': 'button-summary', 'index': 1}, n_clicks=0),
                style={'text-align': 'right'}),
            dbc.Modal([dbc.ModalBody([
                f"Average degree : {props['degrees'][2]:.2f}",
                html.Div(
                    dcc.Graph(figure=scatter_plot([i for i in range(len(props['degrees'][1]))], props['degrees'][1],
                                                  {'x': 'Value', 'y': 'Count'}, 'Degree Distribution'),
                              config=config_modal)
                )])
            ], id={'type': 'modal-summary', 'index': 1}, is_open=False, size='xl')
        ])
    ]))
    items.append(dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P(f"Categories : ")),
            dbc.Col(
                dbc.Button('Show', size='sm', id={'type': 'button-summary', 'index': 2}, n_clicks=0),
                style={'text-align': 'right'}),
            dbc.Modal([dbc.ModalBody([
                f"Number of categories : {len(props['categories'][0])}",
                html.Div(
                    dcc.Graph(
                        figure=bar_chart(list(props['categories'][1].keys()), list(props['categories'][1].values()),
                                         {'x': 'Category', 'y': 'Count'}, 'Category Distribution'),
                        config=config_modal)
                )])
            ], id={'type': 'modal-summary', 'index': 2}, is_open=False, size='xl')
        ])
    ]))
    items.append(dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P(f"Subcategories :")),
            dbc.Col(
                dbc.Button('Show', size='sm', id={'type': 'button-summary', 'index': 3}, n_clicks=0),
                style={'text-align': 'right'}),
            dbc.Modal([dbc.ModalBody([
                f"Number of subcategories : {len(props['subcategories'][0])}",
                html.Div(
                    dcc.Graph(
                        figure=bar_chart(list(props['subcategories'][1].keys()),
                                         list(props['subcategories'][1].values()), {'x': 'Subcategory', 'y': 'Count'},
                                         'Subcategory Distribution'),
                        config=config_modal)
                )])
            ], id={'type': 'modal-summary', 'index': 3}, is_open=False, size='xl')
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
