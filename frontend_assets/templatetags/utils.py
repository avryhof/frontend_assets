from __future__ import unicode_literals

import sys

from django.utils.safestring import mark_safe

if sys.version_info[0] > 2:
    from future.types.newstr import unicode
    from future.standard_library import install_aliases

    # For the future library so we can be Python 2 and 3 compatible
    install_aliases()


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
        retn_list.append('<link rel="stylesheet" href="%s"/>' % css_file)

    return mark_safe('\n'.join(retn_list))


def render_javascript(javascripts):
    retn_list = []

    if not isinstance(javascripts, list):
        javascripts = [javascripts]

    for javascript in javascripts:
        retn_list.append('<script src="%s" type="text/javascript"></script>' % javascript)

    return mark_safe('\n'.join(retn_list))
