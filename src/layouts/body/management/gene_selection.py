from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


def gene_selection(nodes):
    options = [{'label': 'Overview', 'value': 'overview'}]
    options.extend(
        sorted([{'label': node['data']['id'], 'value': node['data']['id']} for node in nodes],
               key=lambda d: d['label']))
    return dbc.Select(
        id='gene_selection',
        options=options,
        placeholder='Choose a gene',
        style={'margin': '10px'}
    )
