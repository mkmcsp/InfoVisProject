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
        autoRefreshLayout=False,
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
                    'height': '5',
                    'width': '5'
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
                    'background-color': 'grey',
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
        ],
        style={
            'width': '100%',
            'height': height
        }
    )
    return fig
