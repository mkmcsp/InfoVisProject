from .filters import *
from .statistics import *
from .gene_selection import gene_selection
from .nodes_mgt import nodes_tab
from .edges_mgt import edges_tab


def tab(content, id, name, style=None):
    return dbc.Tab(content, label=name, tab_id=id, style=style)


def upload_file_modal():
    upload_nodes = html.Div(dcc.Upload(dbc.Button('Choose file containing your nodes', n_clicks=0, color='secondary',
                                                  style={'margin': '5px', 'width': '100%'}), id='upload-data-nodes'))
    upload_edges = html.Div(dcc.Upload(dbc.Button('Choose file containing your edges', n_clicks=0, color='secondary',
                                                  style={'margin': '5px', 'width': '100%'}), id='upload-data-edges'))
    submit = html.Div(
        dbc.Button("Submit", id='submit-file', n_clicks=0, style={'marginTop': '10px', 'align': 'center'}))
    form = dbc.Form([upload_nodes, upload_edges, submit])
    output = dbc.Modal([
        dbc.ModalHeader('Upload your CSV file'),
        dbc.ModalBody(children=dbc.Form(form)),
    ], id='upload_data_modal', is_open=False, style={'textAlign': 'center'}, backdrop='static')
    return output


def management_column(nodes, edges, props):
    return html.Div([
        # Upload file component
        html.Div([
            dbc.Button('Upload a CSV file', id='upload-data', n_clicks=0, style={
                'width': '100%',
                'height': '60px',
                'borderWidth': '1px',
                'textAlign': 'center',
                'margin': '0px 10px 10px 10px',
            }, ),
            upload_file_modal(),
        ]),

        dbc.Tabs(
            [
                tab(nodes_tab, 'nodes-tab', "Nodes", {'marginLeft': '10px'}),
                tab(edges_tab, 'edges-tab', "Edges", {'marginLeft': '10px'})
            ], style={'marginLeft': '10px'}, active_tab='nodes-tab'
        ),
        gene_selection(nodes),
        html.Div(id='gene_selected'),
        dbc.Tabs(
            [
                tab((list_filters(props)), 'filters-tab', "Filters", style={'marginLeft': '10px'}),
                tab(summary(len(nodes), len(edges), props), 'stats-tab', "Stats", style={'marginLeft': '10px'})
            ], style={'marginLeft': '10px', 'marginRight': '10px'}, active_tab='filters-tab'
        ),
    ])
