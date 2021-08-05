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

###################################

def import_csv(f_name, triennale=True):
    """
        Funzione che legge il csv degli orari ottenuto con lo script di Leonardo
        e ritorna un dizionario con una struttura piu' JSON oriented
    """

    years = [1, 2, 3] if triennale else [1, 2]

    f = open( f_name )
    sem = csv.DictReader(f)
    lines = [line for line in sem]

    data = {}
    for Y in years:
        data[Y] = {
            'lunedì': {},
            'martedì': {},
            'mercoledì': {},
            'giovedì': {},
            'venerdì': {}
        }
    
    days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì']
    
    for line in lines:
        anno = int(line["anno"])
        ora = int(line["ora"].split(":")[0])
        for d in days:
            materia = line[d].strip().replace("(","<br />(")
            data[anno][d][ora] = materia if materia != "X" else ""
    
    return data

################################

def write_orari(triennale=True):

    cdl = "triennale" if triennale else "magistrale"

    csv_file = DATA_ROOT + f"{cdl}/{get_current_school_year()}/orario/sem2.csv"

    result_file = SITE_ROOT + f"{cdl}/{get_current_school_year()}/orario.html"

    template_dir = TEMPLATES_ROOT + "orario/"
    template_file = "table.html"

    data = import_csv(csv_file, triennale)
    
    #pprint( data )
    
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( orari=data )
    
    # print( output_from_parsed_template )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )

if __name__ == "__main__":
    write_orari(triennale=True)
    write_orari(triennale=False)

#⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠠⠤⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣀⢤⡒⠉⠁⠀⠒⢂⡀⠀⠀⠀⠈⠉⣒⠤⣀⠀⠀⠀⠀
#⠀⠀⣠⠾⠅⠈⠀⠙⠀⠀⠀⠈⠀⠀⢀⣀⣓⡀⠉⠀⠬⠕⢄⠀⠀
#⠀⣰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠶⢦⡀⠑⠀⠀⠀⠀⠈⢧⠀
#⠀⡇⠀⠀⠀⠀⠀⢤⣀⣀⣀⣀⡀⢀⣀⣀⠙⠀⠀⠀⠀⠀⠀⢸⡄
#⠀⢹⡀⠀⠀⠀⠀⡜⠁⠀⠀⠙⡴⠁⠀⠀⠱⡄⠀⠀⠀⠀⠀⣸⠀
#⠀⠀⠱⢄⡀⠀⢰⣁⣒⣒⣂⣰⣃⣀⣒⣒⣂⢣⠀⠀⠀⢀⡴⠁⠀
#⠀⠀⠀⠀⠙⠲⢼⡀⠀⠙⠀⢠⡇⠀⠛⠀⠀⣌⣀⡤⠖⠉⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢸⡗⢄⣀⡠⠊⠈⢦⣀⣀⠔⡏⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠈⡇⠀⢰⠁⠀⠀⠀⢣⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣠⠔⠊⠉⠁⡏⠀⠀⠀⠀⠘⡆⠤⠿⣄⣀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣧⠸⠒⣚⡩⡇⠀⠀⠀⠀⠀⣏⣙⠒⢴⠈⡇⠀⠀⠀⠀
#⠀⠀⠀⠀⠈⠋⠉⠀⠀⢳⡀⠀⠀⠀⣸⠁⠈⠉⠓⠚⠁⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠛⠛
