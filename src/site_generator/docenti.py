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

def import_courses( triennale=True ):
    """
        Funzione che importa i dati dei corsi
    """
    if triennale:
        f_name = DATA_ROOT + "triennale/20-21/corsi/corsi.csv"
    else:
        f_name = DATA_ROOT + "magistrale/20-21/corsi/corsi.csv"
    
    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def import_teachers(f_name, triennale=True ):
    """
        Funzione che restituisce una lista di dati inerenti ai professori,
        con le seguenti informazioni:
            - homepage -> sito internet del professore
            - insegnamento -> materia insegnata
            - mail -> indirizzo e-mail
            - nome -> nome del professore nel formato 'Cognome Nome'
            - qualifica -> qualifica del docente
            - studio -> numero dello studio
            - telefono -> numero di telefono (dello studio)
            - img-name -> url dell'immagine
            - id-name -> nome del professore nel formato 'cognome-nome'
            - link-corso -> link del corso
    """
    cdl = "triennale" if triennale else "magistrale"

    f = open( f_name )
    sem = csv.DictReader(f)
    lines = [line for line in sem]

    data = []

    info_corsi = import_courses( triennale )

    def get_link( nome_corso ):
        for corso in info_corsi:
            if nome_corso.lower() == corso['insegnamento'].lower():
                # return corso['link']
                return f"{corso['codice']}.html"
        return corso['link']

    def get_teachings(teachings):
        """
        Prende in input una sequenza di materie di insegnamento separate da
        '-' e ritorna una lista di oggetti JSON, ciascuno dei quali
        contiene il nome dell'insegnamento e il link dell'insegnamento.
        """
        res = []
        for teaching in teachings.split("-"):
            res.append({
                'nome': teaching,
                'link-corso': get_link(teaching)
            })
        
        return res


    for d in lines:
        data.append({
            'homepage': get( d['homepage'] ),
            'insegnamenti': get_teachings( d['insegnamenti'] ),
            'mail': get( d['mail'] ),
            'nome': get( d['nome'] ),
            'qualifica': get( d['qualifica'] ),
            'studio': get( d['studio'] ),
            'telefono': get( d['telefono'] ),
            'img-name': img_name(d['nome']),
            'id-name': id_name(d['nome']),
        })

    return data

def get(s):
    """
        Funzione utile per filtrare i campi nulli del file csv.
        Se il campo è nullo ritorna None.
    """
    if s != 'null' and s != '':
        return s
    else:
        return None

def id_name(x):
    """
        Funzione che dato un nome nel formato "Cognome Nome"
        ritorna l'id-name in formato "cognome-nome".
    """
    return x.lower().replace("'","").replace(" ","-")

def img_name(x, extension=".jpg"):
    """
        Funzione che dato un nome nel formato "Cognome Nome"
        ritorna il nome dell'immagine associata al docente.
    """
    return id_name(x) + extension

# -----------------------

def write_docenti(triennale=True):
    cdl = "triennale" if triennale else "magistrale"

    csv_file = {
        "triennale": f"{DATA_ROOT}/triennale/{get_current_school_year()}/docenti/docenti.csv",
        "magistrale": f"{DATA_ROOT}/magistrale/{get_current_school_year()}/docenti/docenti.csv"
    }

    result_file = SITE_ROOT + f"{cdl}/{get_current_school_year()}/docenti.html"

    template_dir = TEMPLATES_ROOT + "docenti/"
    template_file = "card.html"

    data = import_teachers( csv_file[cdl], triennale )

    # pprint( data )
    
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( teachers=data )
    
    # print( output_from_parsed_template )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )

if __name__ == "__main__":
    write_docenti()
    write_docenti(False)