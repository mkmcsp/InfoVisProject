from layouts.body.graphs.utils import *


def random_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    pos = nx.random_layout(G, seed=22)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig


def circular_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    pos = nx.circular_layout(G)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig


def spring_network(id, nodes=None, edges=None):
    G = nx.Graph()
    if nodes is None or edges is None:
        G = nx.petersen_graph()
    pos = nx.spring_layout(G)
    fig = networkx_to_cytoscape(G, pos, id)
    return fig
