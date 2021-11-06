import dash
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH
from dash import html, callback_context
import dash_bootstrap_components as dbc
from layouts.body.management.management_component import management_column
from layouts.body.graphs.nodelink.nodelink import basic_network
from layouts.body.graphs.circular_layout.circular_layout import circular_network
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])


app.layout = html.Div([
    html.H1('InfoVis Project'),
    dbc.Row(
        [
            dbc.Col(management_column, width=3),
            dbc.Col([dbc.ButtonGroup([
                dbc.Button("First"),
                dbc.Button("Second"),
                dbc.Button("Third"),
            ], style={'margin': '19px'})
                , dbc.Card(basic_network(), style={'margin': '19px'})]),
            dbc.Col(dbc.Card(circular_network()), style={'margin': '19px'}),
        ]
    )

], style={'margin': '19px'})


@app.callback(
    Output('upload_data_modal', 'is_open'),
    Input('upload-data', 'n_clicks'),
)
def display_upload_modal(n_clicks):
    if n_clicks == 0:
        return
    return True


@app.callback(
    Output({'type': 'modal', 'index': MATCH}, 'is_open'),
    Input({'type': 'button', 'index': MATCH}, 'n_clicks'),
)
def display_modal(n_clicks):
    # basically if n_clicks = 0 it was not clicked before
    # very important to have this line or else the callback will be triggered whether the button was clicked or not
    if n_clicks == 0:
        return
    # prop_id = ast.literal_eval(callback_context.triggered[0]['prop_id'].split('.')[0])
    return True


@app.callback(
    Output('gene_selected', 'children'),
    Input('gene_selection', 'value'),
)
def display_modal(value):
    if value is None:
        return
    return dbc.Modal(dbc.ModalBody('You have selected {}'.format(value)), is_open=True)


if __name__ == '__main__':
    app.run_server(debug=True)
