"""
@copyright Amos Vryhof

"""
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .utils import join_url, render_css, render_javascript, render_javascript_code

register = template.Library()

static_root = settings.STATIC_URL


@register.simple_tag
def fontawesome4_css():
    font_awesome_url = join_url(static_root, 'css', 'font-awesome-4.min.css')

    return render_css(font_awesome_url)


@register.simple_tag
def fontawesome5_css(shim=False):
    font_awesome_urls = [join_url(static_root, 'css', 'all.min.css')]

    if shim:
        font_awesome_urls.append(join_url(static_root, 'css', 'v4-shims.min.css'))

    return render_css(font_awesome_urls)


@register.simple_tag
def fontawesome5_javascript(shim=False):
    fa_js_url = join_url(static_root, 'js', 'fontawesome.min.js')
    fa_js_all = join_url(static_root, 'js', 'all.min.js')

    javascripts = [fa_js_url, fa_js_all]

    if shim:
        javascripts.append(join_url(static_root, 'js', 'v4-shims.min.js'))

    return render_javascript(javascripts)


@register.simple_tag
def jquery(slim=False):
    if slim:
        jquery_url = join_url(static_root, 'js', 'jquery-3.3.1.slim.min.js')
    else:
        jquery_url = join_url(static_root, 'js', 'jquery-3.3.1.min.js')

    return render_javascript(jquery_url)


@register.simple_tag
def modernizr():
    modernizr_url = join_url(static_root, 'js', 'modernizr.js')

    return render_javascript(modernizr_url)


@register.simple_tag
def ieshiv():
    ieshiv_url = join_url(static_root, 'js', 'ieshiv.js')

    return render_javascript(ieshiv_url)


@register.simple_tag
def leaflet_css():
    leaflet_css_url = join_url(static_root, 'css', 'leaflet.css')

    return render_css(leaflet_css_url)


@register.simple_tag
def leaflet_javascript():
    leaflet_js_url = join_url(static_root, 'js', 'leaflet.js')

    javascripts = [leaflet_js_url]

    return render_javascript(javascripts)


@register.simple_tag
def leaflet_header():
    leafletcss = leaflet_css()
    leafletjs = leaflet_javascript()

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
    code = 'L.marker(%s_marker_coords).addTo(\'%s\');' % (map_prefix, map_id)

    return render_javascript_code([coords, code])
