# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

# -- import all libraries importer in header
from header import *

# ----------------------------------------------

def import_courses(triennale=True):
    cdl = "triennale" if triennale else "magistrale"
    f_name = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/corsi/corsi.csv"
    #path = DATA_ROOT + f"{cdl}/{get_current_school_year()}/corsi"
    #print( os.listdir( path ) )

    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def get_course_data(path, short_name):

    with open(f"{path}/{short_name}.json", "r") as f:
        jo = json.load(f)

        docenti = [{
            "name": name['first_name'] + " " + name['second_name'],
            "id_name": get_id_name(name)
        } for name in jo['docente']]

        # pprint(docenti)

        return {
            'nome':             get(jo["nomeCorso"]),
            'codice':           short_name,
            'docenti':          docenti,
            'anno-accademico':  get(jo['annoAccademico']),
            'crediti':          get(jo['crediti']),
            'settore':          get(jo['settore']),
            'anno':             get(jo['anno']),
            'semestre':         get(jo['semestre']),
            'propedeuticità':   get(jo['propedeuticità']),
            'comunicazioni':    get(jo['comunicazioni']),
            'lezioni':          get(jo['lezioni']),
            'materiale':        get(jo['materiale']),
            'programma':        get(jo['programma']),
            'testi-riferimento':get(jo['testiRiferimento']),
            'ricevimento':      get(jo['ricevimento']),
            'modalita-esame':   get(jo['modalitàEsame'])
        }

def get(s:str):
    """
        Filtra le stringhe "nulle"
    """
    if s != 'null' and s != '' and s!="<table><tr><td>null</td></tr></table>":
        return s
    else:
        return None

def get_id_name(name):
    """
        Funzione che dato un oggetto json della forma 
             {'first_name': A, 'second_name': B},
        ritorna una stringa in formato
            'cognome-nome'
    """
    
    return "-".join(name['second_name'].lower().replace("'", "").split() +
                    name['first_name'].lower().replace("'", "").split())

##########################

def write_courses(triennale=True):
    cdl = "triennale" if triennale else "magistrale"
    courses_dir = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/corsi/"

    data = import_courses(triennale)

    corsi = []
    for d in data:
        corso = get_course_data(courses_dir + f"{d['codice']}", d['codice'])
        corsi.append( corso )
        
    # pprint( corsi )

    template_dir = TEMPLATES_ROOT + "corsi/"
    template_file = "base.html"
    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )

    for corso in corsi:
        result_file = SITE_ROOT + f"{cdl}/{SCHOLAR_YEAR}/{corso['codice']}.html"

        output_from_parsed_template = template.render( data=corso )
        
        #print( output_from_parsed_template )

        # to save the results
        with open(result_file, "w") as fh:
            fh.write( output_from_parsed_template )


##########################

if __name__ == '__main__':
    write_courses() # NON ESEGUIRE CODICE PER MAGISTRALE, BISOGNA GESTIRE QUEL PROBLEMA DEI NOMI
    write_courses(triennale=False)
