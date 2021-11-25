import dash_bootstrap_components as dbc
from dash import html


def edit_tab():
    return dbc.Tab([
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dbc.Switch(
                        id='toggle-label',
                        label="Show/Hide label",
                        value=False
                    ), width=3),
                    dbc.Col(dbc.Input(type='color', value="#FF0000", id='colorpicker-highlight',
                                      style={'width': 35, 'height': 25}), width=1),
                    dbc.Col(dbc.Label('Highlight color'))
                ])
            ])
        )
    ], label='Edit', tab_id='edit_tab')
