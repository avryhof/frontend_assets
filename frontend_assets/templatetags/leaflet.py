def get_tiles(**kwargs):
    provider = kwargs.get('provider', 'openstreetmap').lower()
    lang = kwargs.get('lang', 'EN').upper()


    providers = {
        'openstreetmap': {
            'EN': {
                'tiles': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attr': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, '
                        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
            },
        },
        'mapnik': {
            'EN': {
                'tiles': 'https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
                'attr': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            },
            'DE': {
                'tiles': 'https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
                'attr': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            },
            'CH': {
                'tiles': 'https://tile.osm.ch/switzerland/{z}/{x}/{y}.png',
                'attr': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            },
            'FR': {
                'tiles': 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
                'attr': '&copy; Openstreetmap France | Map data &copy; '
                        '<a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            },
            'HOT': {
                'tiles': 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                'attr': '{attribution.OpenStreetMap},  Tiles style by '
                        '<a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> '
                        'hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
            }
        },
        'openseamap': {
            'EN': {
                'tiles': 'https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
                'attr': 'Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors'

            }
        },
        'opentopomap': {
            'EN': {
                'tiles': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                'attr': 'Map data: {attribution.OpenStreetMap}, '
                        '<a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; '
                        '<a href="https://opentopomap.org">OpenTopoMap</a> '
                        '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'}
        },
        'wikimedia': {
            'EN': {
                'tiles': 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}{r}.png',
                'attr': '<a href="https://wikimediafoundation.org/wiki/Maps_Terms_of_Use">Wikimedia</a>',
            }
        },
    }
