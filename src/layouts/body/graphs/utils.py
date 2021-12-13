import networkx as nx
import community.community_louvain as community_louvain
import math
from collections import Counter

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
        'selector': '.demi-selected',
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
    '''nodes_graph = [
        {'data': {'id': node[0], 'label': node[0]},
         'classes': 'default deg{} com{} bet{} cat{} sub{}'.format(node[1]['degree'], node[1]['community'],
                                                                   node[1]['betweenness'], node[1]['category'],
                                                                   node[1]['subcategory']),
         'position': {'x': 220 * pos[node[0]][0], 'y': -220 * pos[node[0]][1]}} for node in nodes]'''
    nodes_graph = [
        {'data': {'id': node[0], 'label': node[0]},
         'classes': 'default deg{} bet{} brt{} {} sub{}'.format(node[1]['degree'],
                                                                str(node[1]['betweenness']),
                                                                str(int(node[1]['betweenness'] * 10)),
                                                                ' '.join(
                                                                    ['cat{}'.format(item) for item in
                                                                     node[1]['category']]),
                                                                node[1]['subcategory']),
         'position': {'x': 220 * pos[node[0]][0], 'y': -220 * pos[node[0]][1]}} for node in nodes]
    edges_graph = [{'data': {'source': interactorA, 'target': interactorB}} for interactorA, interactorB in edges]
    return nodes_graph, edges_graph


def cytoscape_to_networkx(elements):
    G = nx.Graph()
    G.add_nodes_from([(element['data']['id'],
                       {'degree': element['classes'].split()[1][3:],
                        'category': list(
                            map(lambda x: x[3:], filter(lambda x: x.startswith('cat'), element['classes'].split()))),
                        'subcategory': element['classes'].split()[-1][3:]}) for element in
                      elements if 'source' not in element['data']])
    G.add_edges_from(
        [(element['data']['source'], element['data']['target']) for element in elements if 'source' in element['data']])
    return G


def compute_metrics(G):
    properties = {}
    # communities = community_louvain.best_partition(G)
    # nx.set_node_attributes(G, communities, 'community')
    # properties['communities'] = list(set(communities.values()))
    nx.set_node_attributes(G, {node: val for (node, val) in G.degree}, "degree")
    # [0] = list of unique values, [1] = histogram values, [2] = average
    properties['degrees'] = list(set(dict(G.degree()).values())), nx.degree_histogram(G), sum(
        dict(G.degree()).values()) / len(G.nodes)
    betweenness = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, betweenness, "betweenness")
    properties['betweennesses'] = list(set(betweenness.values()))

    for node in G.nodes(data=True):
        node_dict = node[1]
        if 'category' not in node_dict or (
                not isinstance(node_dict['subcategory'], str) and math.isnan(node_dict['subcategory'])):
            node_dict['category'] = ['Unknown']
        if 'subcategory' not in node_dict or (
                not isinstance(node_dict['subcategory'], str) and math.isnan(node_dict['subcategory'])):
            node_dict['subcategory'] = 'Unknown'
    return G, properties


def preprocess_data(nodes, edges):
    G = nx.Graph()
    nodes_list = [
        (row['OFFICIAL SYMBOL'],
         {'category': [cat.replace(' ', '-') for cat in row['CATEGORY VALUES'].split('|')],
          'subcategory': row['SUBCATEGORY VALUES'].replace(' ', '-') if isinstance(row['SUBCATEGORY VALUES'], str) else
          row['SUBCATEGORY VALUES']})
        for index, row in nodes.iterrows()]
    G.add_nodes_from(nodes_list)

    edges_list = [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
                  edges[:2000].iterrows()]  # temporary!!!!
    G.add_edges_from(edges_list)

    pos = nx.random_layout(G)
    G, props = compute_metrics(G)
    nodes_categories = [cat for index, row in nodes.iterrows() for cat in row['CATEGORY VALUES'].split('|')]
    props['categories'] = list(set(nodes_categories)) + ['Unknown'], Counter(nodes_categories)
    props['categories'][1]['Unknown'] += len(G.nodes) - len(nodes)
    nodes_sub = ['Unknown' if not isinstance(x, str) and math.isnan(x) else x for x in nodes['SUBCATEGORY VALUES']]
    props['subcategories'] = list(set(nodes_sub)), Counter(nodes_sub)
    props['subcategories'][1]['Unknown'] += len(G.nodes) - len(nodes)
    nodes_graph, edges_graph = networkx_to_cytoscape(G.nodes(data=True), G.edges(), pos)

    return nodes_graph, edges_graph, props


def match_node_all_data(node, elements):
    # select all matched edges first
    matched_edges = [element for element in elements if
                     'source' in element['data'] and node in element['data'].values()]
    list_nodes = set([edge['data'][x] for edge in matched_edges for x in ['source', 'target']])
    matched_nodes = [element for element in elements if
                     'id' in element['data'] and element['data']['id'] in list_nodes]

    return matched_nodes + matched_edges


def match_node_only_id(node, elements):
    G = cytoscape_to_networkx(elements)

    if len(G[node]) > 0:
        matched_edges = G.edges(node)
        matched_nodes = [n for n in G[node]] + [node]
    else:
        matched_edges = []
        matched_nodes = [node]
    return matched_nodes, matched_edges


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


def match_filter(node, params):
    degmin, degmax = params['degree']
    return (degmin <= int(node['classes'].split()[1][3:]) <= degmax) and any(
        item in params['categories'] for item in list(map(lambda x: x[3:].replace('-', ' '),
                                                          filter(lambda x: x.startswith('cat'),
                                                                 node['classes'].split())))) and \
           node['classes'].split()[-1][3:].replace('-', ' ') in params['subcategories']


def filter_nodes(elements, elements_without_filter, params):  # elements = current elts, params = dict
    filtered_nodes = [element for element in elements_without_filter if 'source' not in element['data']
                      and match_filter(element, params)]

    list_current_nodes = [element['data']['id'] for element in elements if 'source' not in element['data']]
    for element in filtered_nodes:
        if 'source' not in element['data'] and element['data']['id'] in list_current_nodes:
            element.update([item for item in elements if
                            'source' not in item['data'] and item['data']['id'] == element['data']['id']][0])

    list_nodes = [element['data']['id'] for element in filtered_nodes if 'source' not in element['data']]
    filtered_edges = [element for element in elements_without_filter if
                      'source' in element['data'] and element['data']['source'] in list_nodes and element['data'][
                          'target'] in list_nodes]
    return filtered_nodes + filtered_edges


def get_shortest_path_from_to(elements, source, target):
    G = cytoscape_to_networkx(elements)
    if not nx.has_path(G, source, target):
        return None, None, None, None
    path = nx.shortest_path(G, source, target)
    path = [p for p in path]
    # [1, 2, 3] -> [(1, 2), (2, 3)]
    all_paths_edges = []
    for i in range(len(path) - 1):
        all_paths_edges.append((path[i], path[i + 1]))
    all_paths_nodes = set(path)
    nodes_info = [element for element in elements if
                  'source' not in element['data'] and element['data']['id'] in all_paths_nodes]
    return all_paths_nodes, all_paths_edges, nodes_info, path
