import dash_bootstrap_components as dbc
from dash import html


def edit_tab():
    return dbc.Tab([
        dbc.Card(
            dbc.CardBody([
                dbc.Switch(
                    id='toggle-label',
                    label="Show/Hide label",
                    value=False
                )
            ])
        )
    ], label='Edit', tab_id='edit_tab')
