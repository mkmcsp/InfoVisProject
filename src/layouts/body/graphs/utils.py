import networkx as nx
from random import randrange

default_stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'height': '5',
            'width': '5',
            'text-halign': 'center',
            'text-valign': 'center',
            'font-size': '10px'
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
            'background-color': '#000000',
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


def networkx_to_cytoscape(nodes, edges, pos):
    nodes_graph = [
        {'data': {'id': node, 'label': node}, 'classes': 'default deg{}'.format(randrange(1, 5)),
         'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for node in nodes]
    edges_graph = [{'data': {'source': interactorA, 'target': interactorB}} for interactorA, interactorB in edges]
    return nodes_graph, edges_graph


def cytoscape_to_networkx(elements):
    G = nx.Graph()
    G.add_nodes_from([element['data']['id'] for element in elements if 'source' not in element['data']])
    G.add_edges_from(
        [(element['data']['source'], element['data']['target']) for element in elements if 'source' in element['data']])
    return G


def preprocess_data(nodes, edges, positions):
    G = nx.Graph()
    nodes_list = [
        (row['OFFICIAL SYMBOL'], {'category': row['CATEGORY VALUES'], 'subcategory': row['SUBCATEGORY VALUES']})
        for index, row in nodes.iterrows()]
    G.add_nodes_from(nodes_list)

    edges_list = [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
                  edges.iterrows()]
    G.add_edges_from(edges_list)

    subG = nx.Graph()
    subG.add_nodes_from(G)
    subG.add_edges_from(G.edges)
    subG.remove_nodes_from([node for node, degree in dict(G.degree()).items() if degree < 7])
    # nécessaire ?
    # subG.remove_nodes_from([node for node, degree in dict(G.degree()).items() if degree != 0])

    pos = nx.random_layout(G)
    '''nodes_graph = [
        {'data': {'id': node, 'label': node}, 'classes': 'default deg{}'.format(randrange(1, 5)),
         'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for node in G.nodes()]
    edges_graph = [{'data': {'source': interactorA, 'target': interactorB}} for interactorA, interactorB in G.edges()]'''
    nodes_graph, edges_graph = networkx_to_cytoscape(G.nodes(), G.edges(), pos)
    nodes_subgraph = [{'data': {'id': node['data']['id']}, 'classes': node['classes'],
                       'position': {'x': node['position']['x'], 'y': node['position']['y']}} for node in nodes_graph if
                      node['data']['id'] in subG.nodes()]
    edges_subgraph = [{'data': {'source': edge['data']['source'], 'target': edge['data']['target']}} for edge in
                      edges_graph if edge['data']['source'] in subG.nodes() and edge['data']['target'] in subG.nodes()]
    return nodes_graph + edges_graph, nodes_subgraph + edges_subgraph


def match_node_all_data(node, elements):
    # select all matched edges first
    matched_edges = [element for element in elements if
                     'source' in element['data'] and node in element['data'].values()]
    list_nodes = set([edge['data'][x] for edge in matched_edges for x in ['source', 'target']])
    matched_nodes = [element for element in elements if
                     'id' in element['data'] and element['data']['id'] in list_nodes]

    return matched_nodes + matched_edges


def match_node_only_id(node, elements):
    # select all matched edges first
    matched_edges = [(element['data']['source'], element['data']['target']) for element in elements if
                     'source' in element['data'] and node in element['data'].values()]
    list_nodes = set([edge[x] for edge in matched_edges for x in [0, 1]])
    matched_nodes = [element['data']['id'] for element in elements if
                     'source' not in element['data'] and element['data']['id'] in list_nodes]

    return matched_nodes, matched_edges


def change_layout(elements, layout_selection, *params):
    G = cytoscape_to_networkx(elements)
    if 'spectral' in layout_selection:
        pos = nx.spectral_layout(G)
    nodes, edges = networkx_to_cytoscape(G.nodes(), G.edges, pos)
    return nodes + edges
