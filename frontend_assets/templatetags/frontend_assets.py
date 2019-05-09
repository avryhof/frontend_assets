"""
@copyright Amos Vryhof

"""
import json
import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .utils import join_url, render_css, render_javascript, render_javascript_code

register = template.Library()

static_root = getattr(settings, 'STATIC_URL', '/static/')
use_cdn_default = getattr(settings, 'FRONTEND_USE_CDN', False)

cdn_config_file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static' 'cdn.json'))
cdn_config = json.load(cdn_config_file)
cdn_config_file.close()


@register.simple_tag
def fontawesome4_css(use_cdn=use_cdn_default):
    if use_cdn:
        font_awesome_url = {
            'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
            'integrity': 'sha256-eZrrJcwDc/3uDhsdt61sL2oOBY362qM3lon1gyExkL0='
        }

    else:
        font_awesome_url = join_url(static_root, 'css', 'font-awesome-4.min.css')

    return render_css(font_awesome_url)


@register.simple_tag
def fontawesome5_css(shim=False, use_cdn=use_cdn_default):
    if use_cdn:
        font_awesome_urls = [{
            'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css',
            'integrity': 'sha256-BtbhCIbtfeVWGsqxk1vOHEYXS6qcvQvLMZqjtpWUEx8='
        }]

        if shim:
            font_awesome_urls.append({
                'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/v4-shims.min.css',
                'integrity': 'sha256-D48AdNzxAOgva7Z31xE1yn/NfdqzjqOAzg/5P3CK1QM='
            })

    else:
        font_awesome_urls = [join_url(static_root, 'css', 'all.min.css')]

        if shim:
            font_awesome_urls.append(join_url(static_root, 'css', 'v4-shims.min.css'))

    return render_css(font_awesome_urls)


@register.simple_tag
def fontawesome5_javascript(shim=False, use_cdn=use_cdn_default):
    if use_cdn:
        fa_js_url = {
            'src': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/js/fontawesome.min.js',
            'integrity': 'sha256-KZjyrvXj0bZPo6kaV2/gP3h2LXakV/QALQ6UmBhzqD0='
        }
        fa_js_all = {
            'src': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/js/all.min.js',
            'integrity': 'sha256-JgGtkjMEDh4dZj7UtWqSbUcftdwTFLNR3ih7FH80RHs='
        }

    else:
        fa_js_url = join_url(static_root, 'js', 'fontawesome.min.js')
        fa_js_all = join_url(static_root, 'js', 'all.min.js')

    javascripts = [fa_js_url, fa_js_all]

    if shim:
        if use_cdn:
            javascripts.append( {
                'src': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/js/v4-shims.min.js',
                'integrity': 'sha256-Jk9FySjBvE0bRH9tO3VrPL8zuR+G6AhksO7bEdvXk5w='
            })

        else:
            javascripts.append(join_url(static_root, 'js', 'v4-shims.min.js'))

    return render_javascript(javascripts)


@register.simple_tag
def jquery(slim=False, use_cdn=use_cdn_default):
    if slim:
        if use_cdn:
            jquery_url = {
                'src': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.slim.min.js',
                'integrity': 'sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8='
            }
        else:
            jquery_url = join_url(static_root, 'js', 'jquery-3.3.1.slim.min.js')

    else:
        if use_cdn:
            cdn = cdn_config.get('jquery')
            jquery_url = {
                'src': cdn.get('javascript_url'),
                'integrity': cdn.get('javascript_integrity')
            }
        else:
            jquery_url = join_url(static_root, 'js', 'jquery-3.3.1.min.js')

    return render_javascript(jquery_url)


@register.simple_tag
def modernizr(use_cdn=use_cdn_default):
    if use_cdn:
        cdn = cdn_config.get('modernizr')
        modernizr_url = {
            'src': cdn.get('javascript_url'),
            'integrity': cdn.get('javascript_integrity')
        }
    else:
        modernizr_url = join_url(static_root, 'js', 'modernizr.js')

    return render_javascript(modernizr_url)


@register.simple_tag
def ieshiv():
    ieshiv_url = join_url(static_root, 'js', 'ieshiv.js')

    return render_javascript(ieshiv_url)


@register.simple_tag
def leaflet_css(use_cdn=use_cdn_default):
    if use_cdn:
        cdn = cdn_config.get('leaflet')
        leaflet_css_url = {
            'href': cdn.get('css_url'),
            'integrity': cdn.get('css_integrity')
        }
    else:
        leaflet_css_url = join_url(static_root, 'css', 'leaflet.css')

    return render_css(leaflet_css_url)


@register.simple_tag
def leaflet_javascript(use_cdn=use_cdn_default):
    if use_cdn:
        cdn = cdn_config.get('leaflet')
        leaflet_js_url = {
            'src': cdn.get('javascript_url'),
            'integrity': cdn.get('javascript_integrity')
        }
    else:
        leaflet_js_url = join_url(static_root, 'js', 'leaflet.js')

    javascripts = [leaflet_js_url]

    return render_javascript(javascripts)


@register.simple_tag
def leaflet_header(use_cdn=use_cdn_default):
    leafletcss = leaflet_css(use_cdn)
    leafletjs = leaflet_javascript(use_cdn)

    header_code = leafletcss + leafletjs

    return header_code


@register.simple_tag
def leaflet_map(latitude=None, longitude=None, zoom=16, map_prefix='leaflet', map_tiles=False, map_attr=False):
    if not map_tiles:
        map_tiles = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        map_attr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' \
                   '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
    map_id = '%s_map' % map_prefix
    div = '<div id="%s"></div>' % map_id
    coords = 'var %s_coords = [%s, %s];' % (map_prefix, latitude, longitude)
    map = 'var %s = L.map(\'%s\').setView(%s_coords, %s);' % (map_id, map_id, map_prefix, zoom)
    tile_layer = 'L.tileLayer(\'%s\', {maxZoom: 18, attribution: \'%s\', id: \'%s_streets\'}).addTo(%s);' % (
        map_tiles, map_attr, map_prefix, map_id)

    return mark_safe(div) + render_javascript_code([coords, map, tile_layer])


@register.simple_tag
def leaflet_marker(map_prefix='leaflet', latitude=None, longitude=None):
    map_id = '%s_map' % map_prefix
    coords = 'var %s_marker_coords = [%s, %s];' % (map_prefix, latitude, longitude)
    code = 'L.marker(%s_marker_coords).addTo(%s);' % (map_prefix, map_id)

    return render_javascript_code([coords, code])
