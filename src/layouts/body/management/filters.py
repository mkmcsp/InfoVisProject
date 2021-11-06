from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def list_filters():
    filters = []
    for i in range(7):
        filters.append(dbc.AccordionItem([html.P('Hello {}'.format(i))], title='Category {}'.format(i)))
    return dbc.Card(dbc.CardBody([dbc.Accordion(filters)]))
