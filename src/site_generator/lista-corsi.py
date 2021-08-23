from jinja2 import Environment, FileSystemLoader
import json
import csv
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

def import_courses(triennale=True):
    cdl = "triennale" if triennale else "magistrale"
    f_name = DATA_ROOT + f"{cdl}/{get_current_school_year()}/corsi/corsi.csv"
    #path = DATA_ROOT + f"{cdl}/{get_current_school_year()}/corsi"
    #print( os.listdir( path ) )

    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def compute_courses_data(data, sort_by='anno'):
    corsi = []
    for corso in data:
        corsi.append({
            'nome': corso['insegnamento'],
            'anno': int(corso['anno']),
            'codice': corso['codice'],
            'docente': corso['docente'].replace("-", ", "),
            'cfu': int(corso['CFU'])
            # altri dati in seguito ...
        })
    if sort_by != None:
        try:
            corsi.sort(key=lambda x: x[sort_by])
        except:
            pass
    return corsi

def write_courses_list(triennale=True):
    cdl = "triennale" if triennale else "magistrale"
    corsi = compute_courses_data(import_courses(triennale))
    pprint(corsi)

    template_dir = TEMPLATES_ROOT + "corsi/"
    template_file = "lista.html"
    result_file = SITE_ROOT + f"{cdl}/{get_current_school_year()}/corsi.html"

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( corsi=corsi )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )
    

if __name__ == '__main__':
    write_courses_list()
    write_courses_list(False)