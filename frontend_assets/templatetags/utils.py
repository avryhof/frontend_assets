from __future__ import unicode_literals

import sys
import warnings

import requests
import subresource_integrity
from django.conf import settings
from django.utils.safestring import mark_safe

if sys.version_info[0] > 2:
    from future.types.newstr import unicode
    from future.standard_library import install_aliases

    # For the future library so we can be Python 2 and 3 compatible
    install_aliases()


def get_subresource_integrity(script_path):
    if 'https' in script_path:
        resource = requests.get(script_path, verify=True)
        resource_text = resource.text

    elif 'http' in script_path:
        resource = requests.get(script_path)
        warnings.warn("SRI over HTTP. It is recommended to only load remote scripts over HTTPS.")
        resource_text = resource.text

    else:
        script_file_path = script_path.replace(settings.STATIC_URL, settings.STATIC_ROOT)
        with open(script_file_path, 'r') as sf:
            resource_text = sf.read(sf)
            sf.close()

    return subresource_integrity.render(resource_text)


def join_url(*path_parts):
    path_pieces = []
    path_parts = list(path_parts)

    is_root = False
    if path_parts[0] and path_parts[0][0] == '/':
        is_root = True

    for path_part in path_parts:
        if path_part:
            if isinstance(path_part, (str, unicode)) and '/' in path_part:
                pieces = path_part.split('/')
                path_pieces.append(join_url(*pieces))

            elif isinstance(path_part, (str, unicode)) and '/' not in path_part:
                path_pieces.append(path_part)

    path_string = '/'.join(path_pieces)

    if is_root:
        path_string = '/%s' % path_string

    return path_string


def render_css(css_files):
    retn_list = []

    if not isinstance(css_files, list):
        css_files = [css_files]

    for css_file in css_files:
        if isinstance(css_file, str):
            css_file = {
                'href': css_file,
                'integrity': get_subresource_integrity(css_file)
            }

        if isinstance(css_file, dict):
            href = css_file.get('href', '')
            integrity = css_file.get('integrity')
            if not integrity:
                integrity = get_subresource_integrity(href)

            retn_list.append('<link rel="stylesheet" href="%s" integrity="%s" crossorigin="anonymous" />' % (
                href,
                integrity
            ))

        else:
            retn_list.append('<link rel="stylesheet" href="%s"/>' % css_file)

    return mark_safe('\n'.join(retn_list))


def render_javascript(javascripts):
    retn_list = []

    if not isinstance(javascripts, list):
        javascripts = [javascripts]

    for javascript in javascripts:
        if isinstance(javascript, str):
            javascript = {
                'src': javascript,
                'integrity': get_subresource_integrity(javascript)
            }

        if isinstance(javascript, dict):
            src = javascript.get('src')
            integrity = javascript.get('integrity')
            if not integrity:
                integrity = get_subresource_integrity(src)

            retn_list.append('<script src="%s" integrity="%s" crossorigin="anonymous"></script>' % (
                src,
                integrity
            ))

        else:
            retn_list.append('<script src="%s" type="text/javascript"></script>' % javascript)

    return mark_safe('\n'.join(retn_list))


def render_javascript_code(code_parts):
    code = '\n'.join(code_parts)

    integrity = subresource_integrity.render(code)

    return mark_safe('<script integrity="%s">%s</script>' % (integrity, code))
