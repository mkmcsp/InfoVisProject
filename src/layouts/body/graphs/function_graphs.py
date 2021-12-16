import networkx as nx
import community.community_louvain as community_louvain
import math
from collections import Counter
import json


def networkx_to_cytoscape(nodes, edges, pos):
    nodes_graph = [
        {'data': {'id': node, 'label': node},

         'classes': 'default deg{} com{} bet{} clo{} eig{} brt{} clr{} eir{} {} sub{}'.format(
             dico['degree'], str(dico['community']), str(dico['betweenness']).replace('.', '_'),
             str(dico['closeness']).replace('.', '_'), str(dico['eigenvector']).replace('.', '_'),
             str(int(float(dico['betweenness']) * 10)), str(int(float(dico['closeness']) * 10)),
             str(int(float(dico['eigenvector']) * 10)),
             ' '.join(['cat{}'.format(item) for item in dico['category']]), dico['subcategory']),

         'position': {'x': 220 * pos[node][0], 'y': -220 * pos[node][1]}} for node, dico in nodes]
    edges_graph = [{'data': {'source': interactorA, 'target': interactorB}} for interactorA, interactorB in edges]

    return nodes_graph, edges_graph


def cytoscape_to_networkx(elements):
    G = nx.Graph()
    G.add_nodes_from([(element['data']['id'],
                       {'degree': element['classes'].split()[1][3:],
                        'category': list(
                            map(lambda x: x[3:], filter(lambda x: x.startswith('cat'), element['classes'].split()))),
                        'subcategory': element['classes'].split()[-1][3:].replace('_', '/'),
                        'community': element['classes'].split()[2][3:].replace('_', '.'),
                        'betweenness': element['classes'].split()[3][3:].replace('_', '.'),
                        'closeness': element['classes'].split()[4][3:].replace('_', '.'),
                        'eigenvector': element['classes'].split()[5][3:].replace('_', '.')
                        }) for element in elements if 'source' not in element['data']])

    G.add_edges_from(
        [(element['data']['source'], element['data']['target']) for element in elements if 'source' in element['data']])
    return G


def compute_metrics(G, metrics):
    properties = {}
    nx.set_node_attributes(G, {node: val for (node, val) in G.degree}, "degree")
    # [0] = list of unique values, [1] = histogram values, [2] = average
    properties['degrees'] = sorted(list(set(dict(G.degree()).values()))), nx.degree_histogram(G), sum(
        dict(G.degree()).values()) / len(G.nodes)

    communities = community_louvain.best_partition(G) if metrics is None else metrics[0]
    nx.set_node_attributes(G, communities, 'community')
    properties['communities'] = sorted(list(set(communities.values()))), Counter(list(communities.values()))

    bet = nx.betweenness_centrality(G) if metrics is None else metrics[1]
    betweenness = {node: float('{:.6f}'.format(bt)) for node, bt in bet.items()}
    nx.set_node_attributes(G, betweenness, "betweenness")
    properties['betweennesses'] = sorted(list(set(betweenness.values()))), Counter(list(betweenness.values())), sum(
        betweenness.values()) / len(G.nodes)

    clo = nx.closeness_centrality(G) if metrics is None else metrics[2]
    closeness = {node: float('{:.6f}'.format(cl)) for node, cl in clo.items()}
    nx.set_node_attributes(G, closeness, "closeness")
    properties['closenesses'] = sorted(list(set(closeness.values()))), Counter(list(closeness.values())), sum(
        closeness.values()) / len(G.nodes)

    eig = nx.eigenvector_centrality_numpy(G) if metrics is None else metrics[3]
    eigenvector = {node: float('{:.6f}'.format(ei)) for node, ei in eig.items()}
    nx.set_node_attributes(G, eigenvector, "eigenvector")
    properties['eigenvectors'] = sorted(list(set(eigenvector.values()))), Counter(list(eigenvector.values())), sum(
        eigenvector.values()) / len(G.nodes)

    for node in G.nodes(data=True):
        node_dict = node[1]
        if 'category' not in node_dict or (
                not isinstance(node_dict['category'], list) and math.isnan(node_dict['category'][0])):
            node_dict['category'] = ['Unknown']
        if 'subcategory' not in node_dict or (
                not isinstance(node_dict['subcategory'], str) and math.isnan(node_dict['subcategory'])):
            node_dict['subcategory'] = 'Unknown'
    return G, properties


def preprocess_data(nodes, edges, metrics_file=None):
    G = nx.Graph()
    nodes_list = [
        (row['OFFICIAL SYMBOL'],
         {'category': [cat.replace(' ', '-').replace('/', '_') if isinstance(cat, str) else cat for cat in
                       row['CATEGORY VALUES'].split('|')],
          'subcategory': row['SUBCATEGORY VALUES'].replace(' ', '-').replace('/', '_') if isinstance(
              row['SUBCATEGORY VALUES'], str) else row['SUBCATEGORY VALUES']}) for index, row in nodes.iterrows()]
    G.add_nodes_from(nodes_list)

    edges_list = [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
                  edges.iterrows()]
    G.add_edges_from(edges_list)

    pos = nx.random_layout(G)

    if metrics_file is not None:
        metrics = []
        for file in metrics_file:
            with open(file, 'r') as json_file:
                metrics.append(json.load(json_file))
    else:
        metrics = None

    G, props = compute_metrics(G, metrics)
    nodes_categories = [cat for index, row in nodes.iterrows() for cat in row['CATEGORY VALUES'].split('|')]
    props['categories'] = sorted(list(set(nodes_categories)) + ['Unknown']), Counter(nodes_categories)
    props['categories'][1]['Unknown'] += len(G.nodes) - len(nodes)
    nodes_sub = ['Unknown' if not isinstance(x, str) and math.isnan(x) else x for x in nodes['SUBCATEGORY VALUES']]
    props['subcategories'] = sorted(list(set(nodes_sub))), Counter(nodes_sub)
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


def match_filter(node, params):
    degmin, degmax = params['degree']
    betmin, betmax = params['betweenness']
    clomin, clomax = params['closeness']
    eigmin, eigmax = params['eigenvector']

    return (degmin <= int(node['classes'].split()[1][3:]) <= degmax) and \
           (betmin <= float(node['classes'].split()[3][3:].replace('_', '.')) <= betmax) and \
           (clomin <= float(node['classes'].split()[4][3:].replace('_', '.')) <= clomax) and \
           (eigmin <= float(node['classes'].split()[5][3:].replace('_', '.')) <= eigmax) and \
           int(node['classes'].split()[2][3:]) in params['communities'] and any(
        item in params['categories'] for item in
        list(map(lambda x: x[3:].replace('-', ' ').replace('_', '/'),
                 filter(lambda x: x.startswith('cat'), node['classes'].split())))) and \
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
