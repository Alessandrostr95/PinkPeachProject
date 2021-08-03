#!/usr/bin/env python3

"""This script is used for managing the copying of the assets from the
assets folder to the actual site.

To use it simply execute

  python3 assets.py
"""

import os
from shutil import copyfile
from distutils.dir_util import copy_tree

SITE_ROOT = os.environ['SITE_ROOT']
SRC_ROOT = os.environ['SRC_ROOT']
DATA_ROOT = os.environ['DATA_ROOT']
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT']
ASSETS_ROOT = os.environ['ASSETS_ROOT']

# -- here empty string means SITE_ROOT
FILE_ASSET_MAP = {
    # -- svg
    "logo_TV.svg": ["home/"],
    # -- css
    "css/style.css": ["home/"],
    "css/news-style.css": ["home/"],
    "css/table-style.css": ["home/"],
    "css/tree-style.css": ["home/"],
    # -- js
    "js/script.js": ["home/"],
    "js/docenti.js": ["home/magistrale/20-21/", "home/triennale/20-21/"]
}

DIR_ASSET_MAP = {
    "icons": "",
    "professors-photo": ""
}

if __name__ == "__main__":
    # -- copy assets file
    for f in FILE_ASSET_MAP:
        for path in FILE_ASSET_MAP[f]:
            src = ASSETS_ROOT + f
            basename_f = os.path.basename(f)
            dst = SITE_ROOT + path + basename_f
            copyfile(src, dst)
        
    # -- copy assets dir
    for d in DIR_ASSET_MAP:
        src = ASSETS_ROOT + d
        dst = SITE_ROOT + DIR_ASSET_MAP[d] + d
        copy_tree(src, dst)
