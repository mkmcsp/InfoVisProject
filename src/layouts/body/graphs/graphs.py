from layouts.body.graphs.function_graphs import *
from resources.stylesheet import default_stylesheet
import dash_cytoscape as cyto
import pandas as pd


def network(index, elements):
    height = '400px' if index != 1 else '520px'

    fig = cyto.Cytoscape(
        id={
            'type': 'layout-graph',
            'index': index
        },
        elements=elements,
        autoRefreshLayout=True,
        layout={
            'name': 'preset',
            'positions': {node['data']['id']: node['position'] for node in elements if 'id' in node}
        },
        stylesheet=default_stylesheet,
        style={
            'width': '100%',
            'height': height
        }
    )
    return fig


def change_layout(elements, layout_selection, params):
    G = cytoscape_to_networkx(elements)
    if 'spring' in layout_selection:
        pos = nx.spring_layout(G, k=params[0], iterations=params[1], scale=params[2])

    if 'kamadakawai' in layout_selection:
        pos = nx.kamada_kawai_layout(G, scale=params[0])

    if 'spectral' in layout_selection:
        pos = nx.spectral_layout(G, scale=params[0])

    if 'shell' in layout_selection:
        pos = nx.shell_layout(G, rotate=params[0])

    if 'circular' in layout_selection:
        pos = nx.circular_layout(G, scale=params[0])

    if 'spiral' in layout_selection:
        pos = nx.spiral_layout(G, scale=params[0])

    nodes, edges = networkx_to_cytoscape(G.nodes(data=True), G.edges, pos)
    return nodes + edges