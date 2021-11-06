import dash_cytoscape as cyto
from .stylesheet import stylesheet_nl


def basic_network(nodes=None, edges=None):
    if nodes is None or edges is None:
        return cyto.Cytoscape(
            id='net-graph',
            elements=[
                {'data': {'id': 'one'}, 'position': {'x': 50, 'y': 50}, 'classes': 'temp'},
                {'data': {'id': 'two'}, 'position': {'x': 200, 'y': 200}, 'classes': 'what'},
                {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
            ],
            layout={'name': 'random'},
            stylesheet=[
                {'selector': 'node', 'style': {'content': 'data(label)'}},
                {'selector': '.temp', 'style': {'background-color': 'red'}}
            ]
        )
    nodes_graph = [{'data': {'id': symbol}, 'classes': category} for symbol, category in nodes]
    edges_graph = [{'data': {'source': interactorA, 'target': interactorB} for interactorA, interactorB in edges}]
    circular_graph = cyto.Cytoscape(
        id='circular_net',
        elements=nodes_graph + edges_graph,
        layout={'name': 'random'},
        stylesheet=stylesheet_nl,
    )
    return circular_graph
