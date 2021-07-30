from jinja2 import Environment, FileSystemLoader
import csv
from pprint import pprint

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

    csv_file = ["./sem2.csv", "./sem2_magistrale.csv"]
    result_file = "../../home/index.html"

    triennale = import_csv( csv_file[0] )
    magistrale = import_csv( csv_file[1], degree="Master" )
    pprint( triennale )
    pprint( magistrale )
    
    env = Environment( loader=FileSystemLoader(".") )
    template = env.get_template( './table.html' )
    output_from_parsed_template = template.render( bachelor=triennale, master=magistrale )
    
    print( output_from_parsed_template )

    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )