from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


colors_content = dbc.Card(
    dbc.CardBody(
        [
            html.P('Temporary. What do I have to show here ?')
        ]
    )
)


nodes_tab = dbc.Card(
    dbc.Tabs(
        [
            dbc.Tab(colors_content, label="Temporary"),
        ]
    )
)