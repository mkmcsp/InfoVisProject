from layouts.body.graphs.utils import *


def random_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    if nodes is not None:
        G.add_nodes_from(
            [(row['OFFICIAL SYMBOL'], {'category': row['CATEGORY VALUES'], 'subcategory': row['SUBCATEGORY VALUES']})
             for index, row in nodes.iterrows()])
    if edges is not None:
        G.add_edges_from(
            [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
             edges.iterrows()])
    pos = nx.random_layout(G, seed=22)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig


def circular_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    if nodes is not None:
        G.add_nodes_from(
            [(row['OFFICIAL SYMBOL'], {'category': row['CATEGORY VALUES'], 'subcategory': row['SUBCATEGORY VALUES']})
             for index, row in nodes.iterrows()])
    if edges is not None:
        G.add_edges_from(
            [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
             edges.iterrows()])
    pos = nx.circular_layout(G)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig


def spring_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    if nodes is not None:
        G.add_nodes_from(
            [(row['OFFICIAL SYMBOL'], {'category': row['CATEGORY VALUES'], 'subcategory': row['SUBCATEGORY VALUES']})
             for index, row in nodes.iterrows()])
    if edges is not None:
        G.add_edges_from(
            [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
             edges.iterrows()])
    pos = nx.spring_layout(G)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig
