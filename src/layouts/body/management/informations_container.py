import math
import datetime
import dash_bootstrap_components as dbc
from dash import html


def get_node_info(node, elements):
    return [element for element in elements if node == element['data']['id']][0]


def node_info(node):
    classes = {item[:3]: item[3:].replace('-', ' ') for item in node['classes'].split()[1:] if
               not item.startswith('cat')}
    classes['cat'] = list(
        map(lambda x: x[3:].replace('-', ' '), filter(lambda x: x.startswith('cat'), node['classes'].split())))
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
