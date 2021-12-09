from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def slider_filters(id, elements):
    return html.Div([
        dcc.RangeSlider(
            id=id,
            min=elements[0],
            max=elements[-1],
            value=[elements[0], elements[-1]],
            tooltip={'placement': 'bottom', 'always_visible': True}
        )]
    )


def checkbox_filters(id, elements):
    return html.Div([
        dcc.Checklist(
            options=[{'label': element, 'value': element} for element in sorted(elements)],
            value=elements,
            id=id,
            labelStyle={'display': 'inline-bloc', 'marginLeft': '5px'},
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


def list_filters(props):
    filters = []
    filters.append(dbc.AccordionItem(checkbox_filters('cat-filters', props['categories']), title='Categories settings'))
    filters.append(
        dbc.AccordionItem(checkbox_filters('subcat-filters', props['subcategories']), title='Subcategories settings'))
    filters.append(dbc.AccordionItem(slider_filters('degree-range', props['degrees']), title='Degree settings'))
    '''[dbc.AccordionItem(category_filters(props['categories']), title='Categories settings'),
           dbc.AccordionItem(category_filters(props['subcategories']), title='Subcategories settings'),
           dbc.AccordionItem(degree_filters(props['degrees']), title='Degree settings'),
           dbc.AccordionItem(category_filters(), title='Communities settings'),
           dbc.AccordionItem(betweenness_filters(), title='Betweenness centrality settings'),
           dbc.AccordionItem(eigenvector_filters(), title='Eigenvector centrality settings')]'''
    return dbc.Card(
        dbc.CardBody([dbc.Accordion(filters, start_collapsed=True, flush=True),
                      dbc.Button('Filter', style={'marginTop': '10px', 'float': 'right'}, id='filter-button'),
                      dbc.Button('Reset', color='secondary', style={'marginTop': '10px', 'float': 'left'},
                                 id='reset-button')]))
