from jinja2 import Environment, FileSystemLoader
import feedparser
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

def import_news(f_name):
    data = feedparser.parse(f_name)['entries']

    entries = []
    for d in data:
        entries.append({
            'author': d['author'],
            'date': d['published'][5:-3],
            'title': d['title'],
            'body': {
                'type': d['summary_detail']['type'],
                'value': d['summary']
            },
            'links': [
                {'type': l['type'], 'url': l['url']} for l in d['links']
            ]
        })

    #pprint( entries )
    return entries

def create_tree_data(triennale=True):
    """
        Funzione che genera i dati utili per la costruzione del nav-tree
    """
    cdl = "triennale" if triennale else "magistrale"
    paths = {
        'corsi': DATA_ROOT + f"{cdl}/{get_current_school_year()}/corsi/corsi.csv",
        'docenti': DATA_ROOT + f"{cdl}/{get_current_school_year()}/docenti/docenti.csv"
    }

    tabella_corsi = [line for line in csv.DictReader(open(paths['corsi']))]
    tabella_docenti = [line for line in csv.DictReader(open(paths['docenti']))]

    # pprint( tabella_corsi )
    # pprint( tabella_docenti )

    # processo i corsi
    corsi = {
        1: [],
        2: [],
        3: []
    }
    for corso in tabella_corsi:
        corsi[int(corso['anno'])].append({
            'codice': corso['codice'],
            'docente': corso['docente'],
            'nome': corso['insegnamento'],
            #'link': corso['link']   # inserire link pagina del corso
            'link': SITE_ROOT + f"{cdl}/{get_current_school_year()}/{corso['codice']}.html"
        })
    
    # pprint( corsi )

    # processo i docenti
    docenti = []
    for docente in tabella_docenti:
        docenti.append({
            'nome': docente['nome'],
            'id-name': docente['nome'].lower().replace("'","").replace(" ","-")
        })
    
    #pprint( docenti )

    return {'corsi': corsi, 'docenti': docenti}



if __name__ == "__main__":
    f_names = [
        DATA_ROOT + "triennale/20-21/annunci/triennale.xml",
        DATA_ROOT + "magistrale/20-21/annunci/magistrale.xml"
        ]
    result_file = SITE_ROOT + "home/index.html"
    
    template_dir = TEMPLATES_ROOT + "/home/"
    template_file = "news.html"

    items = {
        "triennale": import_news( f_names[0] ),
        "magistrale": import_news( f_names[1] )
        }

    tree_data = {
        "triennale": create_tree_data(),
        "magistrale": create_tree_data(False)
    }

    # pprint( items)
    # pprint( tree_data )

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( items=items, tree=tree_data, year=get_current_school_year() )
    
    # print( output_from_parsed_template )
    
    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )
