from jinja2 import Environment, FileSystemLoader
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

INVERANALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE = ["invernale", "estiva-anticipata", "estiva", "autunnale"]

def import_exams(sessione, triennale=True):
    cdl = "triennale" if triennale else "magistrale"
    assert sessione in [INVERANALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE]
    f_name = DATA_ROOT + f"{cdl}/{get_current_school_year()}/esami/esami-{sessione}.csv"

    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def compute_exams_data(data, triennale=True):
    """
        sessione <invernale|estiva-anticipata|estiva>
          |
          └──appello <1|2>
               |
               └──anno <1|2|3> => [lista di oggetti]
    """

    cdl = "triennale" if triennale else "magistrale"
    fname_corsi = DATA_ROOT + f"{cdl}/{get_current_school_year()}/corsi/corsi.csv"

    f = open( fname_corsi )
    table = csv.DictReader(f)
    corsi = [line for line in table]
    f.close()

    def get_course_shortname(course_longname):
        for corso in corsi:
            if course_longname.lower() == corso['insegnamento'].lower():
                return corso['codice']
        return ''

    esami = []
    for esame in data:
        esami.append({
            'anno': int(esame['anno']),
            'appello': int(esame['appello']),
            'insegnamento': esame['insegnamento'],
            'codice': get_course_shortname( esame['insegnamento'] ),
            'docente': esame['docente'].replace("-", ", "),
            'orale': {
                'aula': get(esame['orale_aula']),
                'data': get(esame['orale_data']),
                'ora': get(esame['orale_ora'])
            },
            'scritto': {
                'aula': get(esame['scritto_aula']),
                'data': get(esame['scritto_data']),
                'ora': get(esame['scritto_ora'])
            }
        })
    try:
        esami.sort(key=lambda x: (x['anno'], x['appello']))
    except:
        pass
    
    table = {
        1:{1:[],2:[],3:[],},
        2:{1:[],2:[],3:[],}
    }
    for esame in esami:
        table[esame['appello']][esame['anno']].append(esame)

    #return esami
    return table

def get(x:str):
    if x == 'NULL' or x == 'null' or x == 'Null':
        return ''
    return x

def write_exams(triennale=True):
    esami = {
        ESTIVA_ANTICIPATA: compute_exams_data(import_exams(ESTIVA_ANTICIPATA, triennale=triennale), triennale=triennale),
        ESTIVA: compute_exams_data(import_exams(ESTIVA, triennale=triennale), triennale=triennale),
        AUTUNNALE: compute_exams_data(import_exams(AUTUNNALE, triennale=triennale), triennale=triennale)
    }

    # pprint( esami )

    cdl = "triennale" if triennale else "magistrale"
    result_file = SITE_ROOT + f"{cdl}/{get_current_school_year()}/esami.html"

    template_dir = TEMPLATES_ROOT + "esami/"
    template_file = "table.html"


    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render(
        sessioni = [ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE],
        esami = esami,
        AA = get_current_school_year(),
        anni = [1,2,3] if triennale else [1,2]
        )
    
    # print( output_from_parsed_template )
    # {% block tabella scoped %}{% endblock %}

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )

if __name__ == '__main__':
    write_exams()
    write_exams(False)