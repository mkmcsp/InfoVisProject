from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def slider_filters(id, elements, centrality=False):
    return html.Div([
        dcc.RangeSlider(
            id=id,
            min=elements[0],
            max=elements[-1],
            step=1 if not centrality else 0.000001,
            value=[elements[0], elements[-1]],
            tooltip={'placement': 'bottom', 'always_visible': True}
        )]
    )


def checkbox_filters(id, elements):
    return html.Div([
        dcc.Checklist(
            options=[{'label': element, 'value': element} for element in sorted(elements)],
            value=[],
            id=id,
            labelStyle={'display': 'inline-bloc', 'marginLeft': '5px'},
            style={'height': '71px', 'overflow': 'auto'}
        )]
    )


def list_filters(props):
    filters = []
    filters.append(
        dbc.AccordionItem(checkbox_filters('cat-filters', props['categories'][0]), title='Categories settings'))
    filters.append(dbc.AccordionItem(checkbox_filters('subcat-filters', props['subcategories'][0]),
                                     title='Subcategories settings'))
    filters.append(dbc.AccordionItem(slider_filters('degree-range', props['degrees'][0]), title='Degree settings'))
    filters.append(
        dbc.AccordionItem(checkbox_filters('com-filters', props['communities'][0]), title='Communities settings'))
    filters.append(dbc.AccordionItem(slider_filters('bet-filters', props['betweennesses'][0], True),
                                     title='Betweenness Centrality settings'))
    filters.append(dbc.AccordionItem(slider_filters('clo-filters', props['closenesses'][0], True),
                                     title='Closeness Centrality settings'))
    filters.append(dbc.AccordionItem(slider_filters('eig-filters', props['eigenvectors'][0], True),
                                     title='Eigenvector Centrality settings'))
    return dbc.Card(
        dbc.CardBody([dbc.Accordion(filters, start_collapsed=True, flush=True,
                                    style={'height': '445px', 'overflowY': 'auto', 'overflowX': 'hidden'}),
                      dbc.Button('Filter', style={'marginTop': '10px', 'float': 'right'}, id='filter-button'),
                      dbc.Button('Reset', color='warning', style={'marginTop': '10px', 'float': 'left'},
                                 id='reset-button')], style={'height': '510px', 'paddingBottom': '5px'}))
