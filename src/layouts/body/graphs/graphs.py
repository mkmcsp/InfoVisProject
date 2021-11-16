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
        minZoom=0,
        layout={
            'name': 'preset',
            'positions': {node['data']['id']: node['position'] for node in elements if 'id' in node}
        },
        stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'opacity': '0.5',
                    'height': '2',
                    'width': '2'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': '0.5'
                }
            },
        ],
        style={
            'width': '100%',
            'height': height
        }
    )
    return fig
