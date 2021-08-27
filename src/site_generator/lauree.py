from jinja2 import Environment, FileSystemLoader
import json
import os
from pprint import pprint

SITE_ROOT = os.environ['SITE_ROOT'] if "SITE_ROOT" in os.environ else "../../site/"
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT'] if "TEMPLATES_ROOT" in os.environ else "../../templates/"
DATA_ROOT = os.environ['DATA_ROOT'] if "DATA_ROOT" in os.environ else "../../data/"
SRC_ROOT = os.environ['SRC_ROOT'] if "SRC_ROOT" in os.environ else "../../src/"

# -- imported from ../scraper.py
import sys
sys.path.append(SRC_ROOT)

from scraper import get_current_school_year

def import_lauree(triennale=True):
    """
        Data una sessione, legge il file csv degli esami e ritorna una lista di oggetti 'riga'
    """
    cdl = "triennale" if triennale else "magistrale"
    f_name = DATA_ROOT + f"{cdl}/{get_current_school_year()}/lauree/lauree.json"
    
    f = open(f_name, "r")
    lauree = json.load(f)
    f.close()
    
    return lauree
    
def write_lauree(triennale=True):
    # pprint( esami )
    date_lauree = import_lauree(triennale=triennale)
    
    cdl = "triennale" if triennale else "magistrale"
    result_file = SITE_ROOT + f"{cdl}/{get_current_school_year()}/lauree.html"

    template_dir = TEMPLATES_ROOT + "lauree/"
    template_file = "base.html"

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( date_lauree = date_lauree )
    
    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )

if __name__ == '__main__':
    write_lauree()
    write_lauree(False)
