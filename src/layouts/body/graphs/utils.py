import networkx as nx
import plotly.graph_objects as go
import dash_cytoscape as cyto


def network_to_plotly(G, pos):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0 = edge[0]
        pos_x0, pos_y0 = pos[x0]
        x1 = edge[1]
        pos_x1, pos_y1 = pos[x1]
        edge_x.append(pos_x0)
        edge_x.append(pos_x1)
        edge_x.append(None)
        edge_y.append(pos_y0)
        edge_y.append(pos_y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color="pink",
            size=10,
            line_width=2))

    layout = dict(plot_bgcolor='white',
                  paper_bgcolor='white',
                  margin=dict(t=10, b=10, l=10, r=10, pad=0),
                  xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                  yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig


def networkx_to_cytoscape(G, pos, id):
    height = '400px' if id != 'first-graph' else '600px'
    nodes_graph = [{'data': {'id': str(node)}, 'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for node
                   in G.nodes()]
    edges_graph = [{'data': {'source': str(interactorA), 'target': str(interactorB)}} for interactorA, interactorB in
                   G.edges()]
    fig = cyto.Cytoscape(
        id=id,
        elements=nodes_graph + edges_graph,
        zoom=1,
        layout={
            'name': 'preset',
            'positions': {node['data']['id']: node['position'] for node in nodes_graph}
        },
        stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'background-color': 'blue',
                    'opacity': '0.5',
                    'height': '5',
                    'width': '5'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'line-color': 'grey',
                    'width': '1'
                }
            },
        ],
        style={
            'width': '100%',
            'height': height
        }
    )
    return fig
