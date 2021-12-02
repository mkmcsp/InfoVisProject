import networkx as nx
import community.community_louvain as community_louvain
import math

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
    '''nodes_graph = [
        {'data': {'id': node[0], 'label': node[0]},
         'classes': 'default deg{} com{} bet{} cat{} sub{}'.format(node[1]['degree'], node[1]['community'],
                                                                   node[1]['betweenness'], node[1]['category'],
                                                                   node[1]['subcategory']),
         'position': {'x': 220 * pos[node[0]][0], 'y': -220 * pos[node[0]][1]}} for node in nodes]'''
    nodes_graph = [
        {'data': {'id': node[0], 'label': node[0]},
         'classes': 'default deg{} {} sub{}'.format(node[1]['degree'],
                                                    ' '.join(['cat{}'.format(item) for item in node[1]['category']]),
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

    '''    pos = {element['data']['id']: [(element['position']['x'] / 220), (element['position']['y'] / -220)] for element
               in elements if 'source' not in element['data']}'''
    return G


def compute_metrics(G):
    properties = {}
    # communities = community_louvain.best_partition(G)
    # nx.set_node_attributes(G, communities, 'community')
    # properties['communities'] = list(set(communities.values()))
    nx.set_node_attributes(G, {node: val for (node, val) in G.degree}, "degree")
    properties['degrees'] = list(set(dict(G.degree()).values()))
    # betweenness = nx.betweenness_centrality(G)
    # nx.set_node_attributes(G, nx.betweenness_centrality(G), "betweenness")
    # properties['betweennesses'] = list(set(betweenness.values()))
    for node in G.nodes(data=True):
        node_dict = node[1]
        if 'category' not in node_dict or (
                not isinstance(node_dict['category'][0], str) and math.isnan(node_dict['category'][0])):
            node_dict['category'] = ['Unknown']
        if 'subcategory' not in node_dict or (
                not isinstance(node_dict['subcategory'], str) and math.isnan(node_dict['subcategory'])):
            node_dict['subcategory'] = 'Unknown'
    return G, properties


def preprocess_data(nodes, edges, option='all'):
    G = nx.Graph()
    nodes_list = [
        (row['OFFICIAL SYMBOL'],
         {'category': [cat for cat in row['CATEGORY VALUES'].split('|')],
          'subcategory': row['SUBCATEGORY VALUES']})
        for index, row in nodes.iterrows()]
    G.add_nodes_from(nodes_list)

    edges_list = [(row['Official Symbol Interactor A'], row['Official Symbol Interactor B']) for index, row in
                  edges.iterrows()]
    G.add_edges_from(edges_list)

    subG = nx.Graph()
    subG.add_nodes_from(G)
    subG.add_edges_from(G.edges)
    subG.remove_nodes_from([node for node, degree in dict(G.degree()).items() if degree < 22])
    # nécessaire ?

    pos = nx.random_layout(G)
    G, props = compute_metrics(G)
    props['categories'] = list(
        set([cat for index, row in nodes.iterrows() for cat in row['CATEGORY VALUES'].split('|')]))
    props['categories'].append('Unknown')
    props['subcategories'] = ['Unknown' if not isinstance(x, str) and math.isnan(x) else x for x in
                              nodes['SUBCATEGORY VALUES'].unique()]
    nodes_graph, edges_graph = networkx_to_cytoscape(G.nodes(data=True), G.edges(), pos)
    nodes_subgraph = [{'data': {'id': node['data']['id']}, 'classes': node['classes'],
                       'position': {'x': node['position']['x'], 'y': node['position']['y']}} for node in nodes_graph if
                      node['data']['id'] in subG.nodes()]
    edges_subgraph = [{'data': {'source': edge['data']['source'], 'target': edge['data']['target']}} for edge in
                      edges_graph if edge['data']['source'] in subG.nodes() and edge['data']['target'] in subG.nodes()]
    if 'all' in option:
        return nodes_graph + edges_graph, props
    # temporary
    else:
        return nodes_subgraph + edges_subgraph, props


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


def filter_nodes(elements, params):  # params = dict
    # select all matched edges first
    degmin, degmax = params['degree']
    filtered_nodes = [element for element in elements if 'source' not in element['data'] and (
            degmin <= int(element['classes'].split()[1][3:]) <= degmax)]
    list_nodes = [element['data']['id'] for element in filtered_nodes]
    filtered_edges = [element for element in elements if
                      'source' in element['data'] and element['data']['source'] in list_nodes and element['data'][
                          'target'] in list_nodes]
    return filtered_nodes + filtered_edges, elements
