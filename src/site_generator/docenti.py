from jinja2 import Environment, FileSystemLoader
import csv
import os
from pprint import pprint

SITE_ROOT = "../../site/"
DATA_ROOT = "../../data/"
TEMPLATES_ROOT = "../../templates/"
#SITE_ROOT = os.environ['SITE_ROOT']
#SRC_ROOT = os.environ['SRC_ROOT']
#DATA_ROOT = os.environ['DATA_ROOT']
#TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT']

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
    f = open( f_name )
    sem = csv.DictReader(f)
    lines = [line for line in sem]

    data = []

    info_corsi = import_courses( triennale )

    def get_link( nome_corso ):
        for corso in info_corsi:
            if nome_corso.lower() == corso['insegnamento'].lower():
                return corso['link']
        return "#nogo"

    for d in lines:
        data.append({
            'homepage': get( d['homepage'] ),
            'insegnamento': get( d['insegnamento'] ),
            'mail': get( d['mail'] ),
            'nome': get( d['nome'] ),
            'qualifica': get( d['qualifica'] ),
            'studio': get( d['studio'] ),
            'telefono': get( d['telefono'] ),
            'img-name': img_name(d['nome']),
            'id-name': id_name(d['nome']),
            'link-corso': get_link( d['insegnamento'] )
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

if __name__ == "__main__":

    csv_file = [
        DATA_ROOT + "triennale/20-21/docenti/docenti.csv",
        DATA_ROOT + "magistrale/20-21/docenti/docenti.csv"
        ]

    cdl = "triennale"   # cambiare questo per pagina docenti magistrale

    result_file = SITE_ROOT + f"home/{cdl}/20-21/docenti.html"

    template_dir = TEMPLATES_ROOT + "docenti/"
    template_file = "card.html"


    data = import_teachers( csv_file[0] )

    pprint( data )
    
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( teachers=data )
    
    # print( output_from_parsed_template )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )