from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def gene_selection(nodes=None):
    options = [{'label': 'Overview', 'value': 'overview'}]
    if nodes is not None:
        options.extend([{'label': node, 'value': node} for index, node in
                        nodes['OFFICIAL SYMBOL'].sort_values().iteritems()])
    return dbc.Select(
        id='gene_selection',
        options=options,
        placeholder='Choose a gene',
        style={'margin': '10px'}
    )
