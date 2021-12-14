from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
import math


def scatter_plot(x, y, label, title, centrality):
    y = [float('nan') if value == 0 else value for value in y]
    fig = px.scatter(x=x, y=y, labels={'x': label['x'], 'y': label['y']}, title=title)
    fig.update_layout(yaxis_range=[0, math.ceil(max(y) / 10.0) * 10.0])
    if centrality:
        fig.update_xaxes(range=[0, 1])
    return fig


def bar_chart(x, y, label, title):
    fig = px.bar(x=x, y=y, labels={'x': label['x'], 'y': label['y']}, title=title)
    fig = fig.update_layout(yaxis_range=[0, math.ceil(max(y) / 1000.0) * 1000.0])
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    return fig


def stats_item(i, metric, type, type_graph, prop, *params, centrality=False):
    config_modal = {'displaylogo': False, 'modeBarButtonsToRemove': ['sendDataToCloud', 'select2d', 'lasso2d']}
    if type_graph == 'scatterplot':
        fig = scatter_plot(params[0], params[1], {'x': metric, 'y': 'Count'}, f"{metric} Distribution", centrality)
    elif type_graph == 'barchart':
        fig = bar_chart(params[0], params[1], {'x': metric, 'y': 'Count'}, f"{metric} Distribution")
    return dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.P(f"{metric}"), width=9),
            dbc.Col(
                dbc.Button('Show', size='sm', id={'type': 'button-summary', 'index': i}, n_clicks=0),
                style={'text-align': 'right'}, width=3),
            dbc.Modal([dbc.ModalBody([
                f"Average {metric} : {prop[2]}" if type == 'quantitative' else '',
                html.Div(
                    dcc.Graph(figure=fig, config=config_modal)
                )])
            ], id={'type': 'modal-summary', 'index': i}, is_open=False, size='xl')
        ])
    ])


def list_stats(nodes_length, edges_length, props):
    items = []
    items.append(dbc.ListGroupItem([
        html.P(f"Number of nodes : {nodes_length}"),
        html.P(f"Number of edges : {edges_length}")
    ]))

    items.append(stats_item(1, 'Degree', 'quantitative', 'scatterplot', props['degrees'],
                            [i for i in range(len(props['degrees'][1]))], props['degrees'][1]))
    items.append(stats_item(2, 'Community', 'qualitative', 'scatterplot', props['communities'],
                            props['communities'][0], list(props['communities'][1].values())))
    items.append(stats_item(3, 'Category', 'qualitative', 'barchart', props['categories'],
                            list(props['categories'][1].keys()), list(props['categories'][1].values())))
    items.append(stats_item(4, 'Subcategory', 'qualitative', 'barchart', props['subcategories'],
                            list(props['subcategories'][1].keys()), list(props['subcategories'][1].values())))
    items.append(stats_item(5, 'Betweenness Centrality', 'quantitative', 'scatterplot', props['betweennesses'],
                            props['betweennesses'][0], list(props['betweennesses'][1].values()), True))
    items.append(stats_item(6, 'Closeness Centrality', 'quantitative', 'scatterplot', props['closenesses'],
                            props['closenesses'][0], list(props['closenesses'][1].values()), True))
    items.append(stats_item(7, 'Eigenvector Centrality', 'quantitative', 'scatterplot', props['eigenvectors'],
                            props['eigenvectors'][0], list(props['eigenvectors'][1].values()), True))

    return dbc.ListGroup(items, flush=True)


def summary(nodes_length, edges_length, props):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Summary'),
                list_stats(nodes_length, edges_length, props)
            ], style={'height': '510px', 'overflowY': 'auto', 'overflowX': 'hidden'}
        ), id='summary-component'
    )
