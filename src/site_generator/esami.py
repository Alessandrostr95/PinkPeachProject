# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

# -- import all libraries importer in header
from header import *

# ----------------------------------------------

INVERANALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE = ["invernale", "estiva-anticipata", "estiva", "autunnale"]

def import_exams(sessione, triennale=True):
    """
        Data una sessione, legge il file csv degli esami e ritorna una lista di oggetti 'riga'
    """
    cdl = "triennale" if triennale else "magistrale"
    assert sessione in [INVERANALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE]
    f_name = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/esami/esami-{sessione}.csv"

    f = open( f_name )
    sem = csv.DictReader(f)

    return[line for line in sem]

def compute_exams_data(data, triennale=True):
    """
        Data una lista in accordo con quanto ritornato nel metodo 'import_exams'
        struttura i dati nel seguente formato:

        appello <1|2>
            |
            └──anno <1|2|3> => [lista di oggetti]
    """

    cdl = "triennale" if triennale else "magistrale"
    fname_corsi = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/corsi/corsi.csv"

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
        1:{1:[],2:[],3:[]},
        2:{1:[],2:[],3:[]}
    }
    for esame in esami:
        table[esame['appello']][esame['anno']].append(esame)

    #return esami
    return table

def get(x:str):
    if x == 'NULL' or x == 'null' or x == 'Null' or x == '':
        return None
    return x

def write_exams(triennale=True):
    esami = {
        ESTIVA_ANTICIPATA: compute_exams_data(import_exams(ESTIVA_ANTICIPATA, triennale=triennale), triennale=triennale),
        ESTIVA: compute_exams_data(import_exams(ESTIVA, triennale=triennale), triennale=triennale),
        AUTUNNALE: compute_exams_data(import_exams(AUTUNNALE, triennale=triennale), triennale=triennale)
    }
    """
        L'oggetto esami ha la seguente struttura
        sessione <invernale|estiva-anticipata|estiva>
          |
          └──appello <1|2>
               |
               └──anno <1|2|3> => [lista di oggetti]
    """

    # pprint( esami )

    cdl = "triennale" if triennale else "magistrale"
    result_file = SITE_ROOT + f"{cdl}/{SCHOLAR_YEAR}/esami.html"

    template_dir = TEMPLATES_ROOT + "esami/"
    template_file = "table.html"


    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render(
        sessioni = [ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE],
        esami = esami,
        AA = SCHOLAR_YEAR,
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
