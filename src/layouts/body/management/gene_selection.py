from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

gene_select = dbc.Select(
    class_name='form-select',
    id='gene_selection',
    options=[
        {'label': 'Overview', 'value': 'overview'},
        {'label': 'Gene 1', 'value': 'gene 1'},
        {'label': 'Gene 2', 'value': 'gene 2'},
        {'label': 'Gene 3', 'value': 'gene 3'},
    ],
    placeholder='Choose a gene',
    style={'margin': '10px'}
)
