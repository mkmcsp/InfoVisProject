from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def gene_selection():
    options = [{'label': 'Overview', 'value': 'overview'}]
    return dbc.Select(
        id='gene_selection',
        options=options,
        placeholder='Choose a gene',
        style={'margin': '10px'}
    )
