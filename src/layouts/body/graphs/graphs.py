from layouts.body.graphs.utils import *
import dash_cytoscape as cyto


def network(index, elements):
    height = '400px' if index != 1 else '520px'

    fig = cyto.Cytoscape(
        id={
            'type': 'layout-graph',
            'index': index
        },
        elements=elements,
        # Should I remove ?
        autoRefreshLayout=True,
        minZoom=0,
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
