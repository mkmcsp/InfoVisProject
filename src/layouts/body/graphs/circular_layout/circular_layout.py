import dash_cytoscape as cyto
from .stylesheet import stylesheet_circular


def circular_network(nodes=None, edges=None):
    if nodes is None or edges is None:
        return cyto.Cytoscape(
            id='circular-graph',
            elements=[
                {'data': {'id': 'one'}, 'position': {'x': 50, 'y': 50}, 'classes': 'temp'},
                {'data': {'id': 'two'}, 'position': {'x': 200, 'y': 200}, 'classes': 'what'},
                {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
            ],
            layout={'name': 'circle'},
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
        layout={'name': 'circle'},
        stylesheet=stylesheet_circular,
    )
    return circular_graph
