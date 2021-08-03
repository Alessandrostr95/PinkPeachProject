from jinja2 import Environment, FileSystemLoader
import csv
import os
from pprint import pprint

SITE_ROOT = os.environ['SITE_ROOT'] if "SITE_ROOT" in os.environ else "../../site/"
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT'] if "TEMPLATES_ROOT" in os.environ else "../../templates/"
DATA_ROOT = os.environ['DATA_ROOT'] if "DATA_ROOT" in os.environ else "../../data/"
SRC_ROOT = os.environ['SRC_ROOT'] if "SRC_ROOT" in os.environ else "../../src/"

def import_csv(f_name, degree="Triennale"):
    """
        Funzione che legge il csv degli orari ottenuto con lo script di Leonardo
        e ritorna un dizionario con una struttura piu' JSON oriented
    """

    years = [1, 2, 3] if degree == "Triennale" else [1, 2]

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


if __name__ == "__main__":
    csv_file = [DATA_ROOT + "triennale/20-21/orario/sem2.csv",
                DATA_ROOT + "magistrale/20-21/orario/sem2.csv"]

    result_file = SITE_ROOT + "home/orario.html"

    template_dir = TEMPLATES_ROOT + "orario"
    template_file = "table.html"


    triennale = import_csv( csv_file[0] )
    magistrale = import_csv( csv_file[1], degree="Master" )
    
    pprint( triennale )
    pprint( magistrale )
    
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( bachelor=triennale, master=magistrale )
    
    print( output_from_parsed_template )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )
