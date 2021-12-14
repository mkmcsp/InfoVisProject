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