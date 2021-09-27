import os
import sys

from jinja2 import Environment, FileSystemLoader
from pprint import pprint
from datetime import datetime
from enum import Enum

import csv
import feedparser
import requests
import json

SITE_ROOT = os.environ['SITE_ROOT'] if "SITE_ROOT" in os.environ else "../../site/"
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT'] if "TEMPLATES_ROOT" in os.environ else "../../templates/"
DATA_ROOT = os.environ['DATA_ROOT'] if "DATA_ROOT" in os.environ else "../../data/"
SRC_ROOT = os.environ['SRC_ROOT'] if "SRC_ROOT" in os.environ else "../../src/"

class Degree(Enum):
    BACHELOR = 1
    MASTER = 2

# ----------------------------------------------

sys.path.append(SRC_ROOT)
from scraper import get_current_school_year

SCHOLAR_YEAR = "21-22"  # "20-21" # "f{get_current_school_year()}"
