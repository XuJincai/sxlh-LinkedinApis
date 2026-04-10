import json
import sys
from os import path

import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = path.dirname(__file__)

try:
    sign_path = path.join(basedir, 'static', 'Linkein.js')
    node_modules = path.join(basedir, 'static', 'node_modules')
    sign_js = execjs.compile(open(sign_path, 'r', encoding='utf-8').read(), cwd=node_modules)
except:
    sign_path = path.join(basedir, '..', 'static', 'Linkein.js')
    node_modules = path.join(basedir, '..', 'static', 'node_modules')
    sign_js = execjs.compile(open(sign_path, 'r', encoding='utf-8').read(), cwd=node_modules)

def trans_cookies(cookies_str):
    cookies = dict()
    for i in cookies_str.split("; "):
        try:
            cookies[i.split('=')[0]] = '='.join(i.split('=')[1:])
        except:
            continue
    return cookies

def generate_requests_params(data):
    data = sign_js.call('generateRequestParams', data)
    data = json.dumps(data, separators=(',', ':'))
    return data

def generate_trackingId(uuid):
    trackingId = sign_js.call('Fl', uuid)
    return trackingId


def splice_url(url, params):
    url += '?'
    for k, v in params.items():
        url += f'{k}={v}&'
    return url[:-1]
