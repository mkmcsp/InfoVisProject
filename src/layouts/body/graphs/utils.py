import networkx as nx


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
    nodes_graph = [{'data': {'id': str(node)}, 'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for
                   node in G.nodes()]
    edges_graph = [{'data': {'source': str(interactorA), 'target': str(interactorB)}} for interactorA, interactorB
                   in G.edges()]
    return nodes_graph + edges_graph
