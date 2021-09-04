# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

# -- import all libraries importer in header
from header import *

# ------------------------------

def import_courses( triennale=True ):
    """
        Funzione che importa i dati dei corsi
    """
    if triennale:
        f_name = DATA_ROOT + f"triennale/{SCHOLAR_YEAR}/corsi/corsi.csv"
    else:
        f_name = DATA_ROOT + f"magistrale/{SCHOLAR_YEAR}/corsi/corsi.csv"
    
    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

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
    
    info_corsi = import_courses( triennale )

    def get_link( nome_corso ):
        for corso in info_corsi:
            if nome_corso.lower() == corso['insegnamento'].lower():
                return corso['codice'] + ".html"
        return "#nogo"
    
    
    days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì']
    
    for line in lines:
        anno = int(line["anno"])
        ora = int(line["ora"].split(":")[0])
        #ora = line["ora"]
        for d in days:
            materia = line[d].strip().replace("(","<br />(")
            data[anno][d][ora] = {
                "entry": materia if materia != "X" else "",
                "link": get_link( line[d].strip().split("(")[0] )  # cambiare questo per inserire il link alla pagina del corso
                }
    
    return data

################################

def write_orari(triennale=True):

    cdl = "triennale" if triennale else "magistrale"

    csv_file = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/orario/sem2.csv"

    result_file = SITE_ROOT + f"{cdl}/{SCHOLAR_YEAR}/orario.html"

    template_dir = TEMPLATES_ROOT + "orario/"
    template_file = "table.html"

    data = import_csv(csv_file, triennale)
    
    #pprint( data )
    
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render(
        orari=data,
        H=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        )
    
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
