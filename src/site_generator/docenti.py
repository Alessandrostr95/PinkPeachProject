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
    if triennale:
        f_name = DATA_ROOT + "triennale/20-21/corsi/corsi.csv"
    else:
        f_name = DATA_ROOT + "magistrale/20-21/corsi/corsi.csv"
    
    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def import_teachers(f_name, triennale=True ):

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
    if s != 'null' and s != '':
        return s
    else:
        return None

def id_name(x):
    return x.lower().replace("'","").replace(" ","-")

def img_name(x, extension=".jpg"):
    return id_name(x) + extension

if __name__ == "__main__":

    csv_file = [
        DATA_ROOT + "triennale/20-21/docenti/docenti.csv",
        DATA_ROOT + "magistrale/20-21/docenti/docenti.csv"
        ]

    result_file = SITE_ROOT + "home/docenti.html"

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