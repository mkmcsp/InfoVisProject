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
    classes = {item[:3]: item[3:].replace('-', ' ') for item in node['classes'].split()[1:] if
               not item.startswith('cat')}
    classes['cat'] = list(
        map(lambda x: x[3:].replace('-', ' '), filter(lambda x: x.startswith('cat'), node['classes'].split())))
    return classes


def node_path_info(node):
    classes = extract_attributes_from(node)
    return html.Div([
        html.Div(f"ID : {node['data']['id']}"),
        html.Div(f"Degree : {classes['deg']}"),
        html.Div(f"Category(ies) : {', '.join(classes['cat'])}"),
        html.Div(f"Subcategory : {classes['sub']}")
    ])


def node_info(node):
    classes = extract_attributes_from(node)
    return dbc.Table([
        html.Thead(html.Tr([
            html.Th('ID'), html.Th('Degree'), html.Th('Category(ies)'), html.Th('Subcategory')
        ])),
        html.Tbody([
            html.Tr([
                html.Td(node['data']['id']),
                html.Td(classes['deg']),
                html.Td(', '.join(classes['cat'])),
                html.Td(classes['sub']),
            ])
        ])
    ], size='sm', style={'textAlign': 'center'})
