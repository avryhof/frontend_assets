"""
@copyright Amos Vryhof

"""
from django import template
from django.conf import settings

from frontend_assets.utils import join_url, render_css, render_javascript

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
def modernizr():
    modernizr_url = join_url(static_root, 'js', 'modernizr.js')

    return render_javascript(modernizr_url)


@register.simple_tag
def ieshiv():
    ieshiv_url = join_url(static_root, 'js', 'ieshiv.js')

    return render_javascript(ieshiv_url)
