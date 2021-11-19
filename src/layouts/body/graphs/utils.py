import networkx as nx
from random import randrange

default_stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'height': '5',
            'width': '5'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': '0.5'
        }
    },
    {
        'selector': '.default',
        'style': {
            'background-color': 'grey',
        }
    },
    {
        'selector': '.selected',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.sub-selected',
        'style': {
            'background-color': 'red',
            'opacity': '0.2'
        }
    },
    {
        'selector': '.not-selected',
        'style': {
            'opacity': '0.2'
        }
    },
]


def preprocess_data(nodes, edges, positions):
    # temporary
    if 'nodes' in nodes and 'edges' in edges:
        nodes = None
        edges = None
    G = nx.Graph()
    if nodes is None and edges is None:
        G = nx.petersen_graph()
    if nodes is not None:
        G.add_nodes_from(
            [(row['OFFICIAL SYMBOL'], {'category': row['CATEGORY VALUES'], 'subcategory': row['SUBCATEGORY VALUES']})
             for index, row in nodes.iterrows()])
    if edges is not None:
        G.add_edges_from(
            [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
             edges.iterrows()])
    if 'random' in positions:
        pos = nx.random_layout(G, seed=22)
    nodes_graph = [{'data': {'id': str(node)}, 'classes': 'default deg' + str(randrange(1, 5)),
                    'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for node in G.nodes()]
    edges_graph = [{'data': {'source': str(interactorA), 'target': str(interactorB)}} for interactorA, interactorB
                   in G.edges()]
    return nodes_graph + edges_graph


def match_node(node, elements):
    # select all matched edges first
    matched_edges = [element for element in elements if
                     'source' in element['data'] and node in element['data'].values()]
    list_nodes = set([edge['data'][x] for edge in matched_edges for x in ['source', 'target']])
    matched_nodes = [element for element in elements if
                     'id' in element['data'] and element['data']['id'] in list_nodes]

    return matched_nodes + matched_edges
