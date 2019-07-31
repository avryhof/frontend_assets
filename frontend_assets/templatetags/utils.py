from __future__ import unicode_literals

import os
import re
import sys
import warnings

import requests
import subresource_integrity
from django.conf import settings
from django.utils.safestring import mark_safe

static_url = getattr(settings, "STATIC_URL", "/static/")
static_path = getattr(settings, "STATIC_ROOT", False)

if sys.version_info[0] > 2:
    from future.standard_library import install_aliases

    # For the future library so we can be Python 2 and 3 compatible
    install_aliases()


def find_static_file(relative_path):
    static_dirs = list(getattr(settings, "STATICFILES_DIRS", []))
    static_dirs.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"))
    for static_dir in static_dirs:
        actual_path = os.path.join(static_dir, relative_path)
        if os.path.exists(actual_path):
            return actual_path
    return False


def path_explode(path_string):
    return re.split(r"/|\\", path_string)


def get_subresource_integrity(script_path):
    retn = ""

    is_https = "https" in script_path
    if "http" in script_path:
        resource = requests.get(script_path, verify=is_https)
        if not is_https:
            warnings.warn("SRI over HTTP. It is recommended to only load remote scripts over HTTPS.")
        resource_text = resource.text

    else:
        relative_path = script_path.replace(static_url, "")
        script_file_path = find_static_file(relative_path)

        if script_file_path:
            with open(script_file_path, "r") as sf:
                resource_text = sf.read()
                sf.close()

            retn = subresource_integrity.render(resource_text.encode())

    return retn


def join_url(*args):
    os_path = os.path.join(*args)
    path_parts = path_explode(os_path)

    return "/".join(path_parts)


def render_css(css_files):
    retn_list = []

    if not isinstance(css_files, list):
        css_files = [css_files]

    for css_file in css_files:
        if isinstance(css_file, str):
            css_file = {"href": css_file, "integrity": get_subresource_integrity(css_file)}

        if isinstance(css_file, dict):
            href = css_file.get("href", "")
            integrity = css_file.get("integrity")
            if not integrity:
                integrity = get_subresource_integrity(href)

            retn_list.append(
                '<link rel="stylesheet" href="%s" integrity="%s" crossorigin="anonymous" />' % (href, integrity)
            )

        else:
            retn_list.append('<link rel="stylesheet" href="%s"/>' % css_file)

    return mark_safe("\n".join(retn_list))


def render_javascript(javascripts):
    retn_list = []

    if not isinstance(javascripts, list):
        javascripts = [javascripts]

    for javascript in javascripts:
        if isinstance(javascript, str):
            javascript = {"src": javascript, "integrity": get_subresource_integrity(javascript)}

        if isinstance(javascript, dict):
            src = javascript.get("src")
            integrity = javascript.get("integrity")
            if not integrity:
                integrity = get_subresource_integrity(src)

            retn_list.append('<script src="%s" integrity="%s" crossorigin="anonymous"></script>' % (src, integrity))

        else:
            retn_list.append('<script src="%s" type="text/javascript"></script>' % javascript)

    return mark_safe("\n".join(retn_list))


def render_javascript_code(code_parts):
    code = "\n".join(code_parts)

    integrity = subresource_integrity.render(code)

    return mark_safe('<script integrity="%s">%s</script>' % (integrity, code))
