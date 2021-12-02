from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def degree_filters(nodes=None):
    return html.Div([
        dcc.RangeSlider(
            id='degree-range',
            min=1,
            max=2500,
            value=[0, 2500],
            tooltip={'placement': 'bottom', 'always_visible': True}
        )]
    )


def category_filters(nodes=None):
    return html.Div([
        dcc.Checklist(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value=['NYC', 'MTL', 'SF'],
            labelStyle={'display': 'inline-bloc'},
            style={'height': '71px', 'overflow': 'auto'}
        )]
    )


def betweenness_filters(nodes=None):
    return html.Div([
        dcc.RangeSlider(
            min=0.0,
            max=1.0,
            step=0.01,
            value=[0.0, 0.7],
            tooltip={'placement': 'bottom', 'always_visible': True}
        )]
    )


def eigenvector_filters(nodes=None):
    return html.Div([
        dcc.RangeSlider(
            min=0.0,
            max=1.0,
            step=0.01,
            value=[0.0, 0.7],
            tooltip={'placement': 'bottom', 'always_visible': True}
        )]
    )


def list_filters():
    filters = []
    filters.append(dbc.AccordionItem(category_filters(), title='Categories settings'))
    filters.append(dbc.AccordionItem(category_filters(), title='Subcategories settings'))
    filters.append(dbc.AccordionItem(category_filters(), title='Communities settings'))
    filters.append(dbc.AccordionItem(degree_filters(), title='Degree settings'))
    filters.append(dbc.AccordionItem(betweenness_filters(), title='Betweenness centrality settings'))
    filters.append(dbc.AccordionItem(eigenvector_filters(), title='Eigenvector centrality settings'))
    return dbc.Card(dbc.CardBody([dbc.Accordion(filters), dbc.Button('Filter', style={'marginTop': '10px'}, id='filter-button')]))
