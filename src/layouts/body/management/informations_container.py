import math
import datetime
import dash_bootstrap_components as dbc
from dash import html


def get_node_info(node, elements):
    return [element for element in elements if 'id' in element['data'] and node == element['data']['id']][0]


def path_info(nodes, path):
    items = [html.Span(
        [dbc.Button(node, id=f"{node}-target", style={'margin': '5px'}),
         html.I(className="bi bi-arrow-right")]) if index != len(
        path) - 1 else dbc.Button(node, id=f"{node}-target", style={'margin': '5px'}) for index, node in
             enumerate(path)]
    items.extend(
        [dbc.Tooltip(node_path_info(node), target=f"{node['data']['id']}-target", placement='bottom',
                     style={'textAlign': 'left'}) for node in nodes])
    return html.Div(items)


def extract_attributes_from(node):
    classes = {
        item[:3]: item[3:].replace('-', ' ').replace('_', '/') if item[:3] not in ['bet', 'clo', 'eig'] else item[
                                                                                                             3:].replace(
            '_', '.') for item in node['classes'].split()[1:] if item[:3] not in ['cat', 'brt', 'clr', 'eir']}
    classes['cat'] = list(
        map(lambda x: x[3:].replace('-', ' ').replace('_', '/'),
            filter(lambda x: x.startswith('cat'), node['classes'].split())))
    return classes


def node_path_info(node):
    classes = extract_attributes_from(node)
    return html.Div([
        html.Div(f"ID : {node['data']['id']}"),
        html.Div(f"Degree : {classes['deg']}"),
        html.Div(f"Category(ies) : {', '.join(classes['cat'])}"),
        html.Div(f"Subcategory : {classes['sub']}"),
        html.Div(f"Community : {classes['com']}"),
        html.Div(f"Betweenness Centrality : {classes['bet']}"),
        html.Div(f"Closeness Centrality : {classes['clo']}"),
        html.Div(f"Eigenvector Centrality : {classes['eig']}")
    ])


def node_info(node):
    classes = extract_attributes_from(node)
    return html.Div([
        dbc.Row([
            dbc.Col('ID:', width=2),
            dbc.Col(node['data']['id'], width=4),
            dbc.Col('DEG:', id='deg-th', width=2),
            dbc.Col(classes['deg'])
        ]),
        dbc.Row([
            dbc.Col('COM:', id='com-th', width=2),
            dbc.Col(classes['com'], width=4),
            dbc.Col('BEC:', id='bet-th', width=2),
            dbc.Col(classes['bet'], width=4)
        ]),
        dbc.Row([
            dbc.Col('CLC:', id='clo-th', width=2),
            dbc.Col(classes['clo'], width=4),
            dbc.Col('EIC:', id='eig-th', width=2),
            dbc.Col(classes['eig'], width=4)
        ]),
        dbc.Row([
            dbc.Col('CAT:', id='cat-th', width=2),
            dbc.Col(', '.join(classes['cat']), width=4),
            dbc.Col('SUB:', id='sub-th', width=2),
            dbc.Col(classes['sub'], width=4)
        ]),
        dbc.Tooltip('Degree', target='deg-th', placement='top'),
        dbc.Tooltip('Category(ies)', target='cat-th', placement='top'),
        dbc.Tooltip('Subcategory', target='sub-th', placement='top'),
        dbc.Tooltip('Community', target='com-th', placement='top'),
        dbc.Tooltip('Betweenness Centrality', target='bet-th', placement='top'),
        dbc.Tooltip('Closeness Centrality', target='clo-th', placement='top'),
        dbc.Tooltip('Eigenvector Centrality', target='eig-th', placement='top'),
    ], style={'textAlign': 'center', 'width': '390px'})
