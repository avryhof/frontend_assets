import json
import os
import pprint

import requests

from frontend_assets.templatetags.utils import get_subresource_integrity


def download_script(script_url):
    script_filename = script_url.split('/')[-1]
    script_type = script_filename.split('.')[-1]

    target_path = os.path.join('frontend_assets', 'static', script_type, script_filename)
    file_contents = requests.get(script_url)

    try:
        with open(target_path, 'w') as t:
            t.write(file_contents.text)
            t.close()
    except IOError:
        print(script_url, target_path)


scripts = ['jquery', 'leaflet', 'modernizr']
# scripts = ['font-awesome::all,v4-shims']

target_path = os.path.join('frontend_assets', 'static', 'cdn.json')
with open(target_path, 'w') as cdn_json:
    json_dict = dict()

    for script in scripts:
        requested_version = False
        files = []

        if ':' in script:
            script, requested_version = script.split(':')

        resource_url = 'https://cdnjs.cloudflare.com/ajax/libs/%s' % script
        src_url = ' https://api.cdnjs.com/libraries/%s' % script
        page_resp = requests.get(src_url)
        resp = page_resp.json()

        version = resp.get('version')
        if requested_version:
            version = requested_version

        assets = resp.get('assets')

        for asset in assets:
            assets_version = asset.get('version')
            if assets_version.startswith(version):
                resource_url = 'https://cdnjs.cloudflare.com/ajax/libs/%s/%s/' % (script, version)
                files = asset.get('files')
                break

        javascript_file = None
        javascript_min_file = None
        css_file = None
        css_min_file = None

        min_js = '%s.min.js' % script
        js = '%s.js' % script
        min_css = '%s.min.css' % script
        css = '%s.css' % script

        for script_file in files:
            if min_js in script_file and not javascript_min_file:
                javascript_min_file = script_file

            elif min_css in script_file and not css_min_file:
                css_min_file = script_file

            elif js in script_file and not javascript_file:
                javascript_file = script_file

            elif css in script_file and not css_file:
                css_file = script_file

        for dl in [javascript_min_file, javascript_file, css_min_file, css_file]:
            if dl:
                target_url = '%s%s' % (resource_url, dl)
                download_script(target_url)

        script_dict = {
            'version': version,
            'base_url': resource_url,
        }

        javascript_url = None
        css_url = None

        if javascript_min_file:
            javascript_url = '%s%s' % (resource_url, javascript_min_file)

        if not javascript_url and javascript_file:
            javascript_url = '%s%s' % (resource_url, javascript_file)

        if javascript_url:
            script_dict.update({'javascript_url': javascript_url})
            script_dict.update({'javascript_integrity': get_subresource_integrity(javascript_url)})

        if css_min_file:
            css_url = '%s%s' % (resource_url, css_min_file)

        if not css_url and css_file:
            css_url = '%s%s' % (resource_url, css_file)

        if css_url:
            script_dict.update({'css_url': css_url})
            script_dict.update({'css_integrity': get_subresource_integrity(css_url)})

        json_dict.update({script: script_dict})

    json.dump(json_dict, cdn_json)

    cdn_json.close()
