# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

from header import Degree

# -- import all libraries importer in header
from header import *

from utils import get_degree_years
from utils import get_degree_pathname
from utils import write_output
from utils import read_csv

# ----------------------------------------------

INVERNALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE = ["invernale", "estiva-anticipata", "estiva", "autunnale"]

def import_exams(session, degree):
    """
        Data una sessione, legge il file csv degli esami e ritorna una lista di oggetti 'riga'
    """
    assert session in [INVERNALE, ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE]
    
    f_name = DATA_ROOT + f"{get_degree_pathname(degree)}/{SCHOLAR_YEAR}/esami/esami-{session}.csv"
    return read_csv(f_name)

def compute_exams_data(data, degree):
    """
        Data una lista in accordo con quanto ritornato nel metodo 'import_exams'
        struttura i dati nel seguente formato:

        appello <1|2>
            |
            └──anno <1|2|3> => [lista di oggetti]
    """

    fname_corsi = DATA_ROOT + f"{get_degree_pathname(degree)}/{SCHOLAR_YEAR}/corsi/corsi.csv"
    corsi = read_csv(fname_corsi)

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

def generate_exams(degree):
    esami = {
        ESTIVA_ANTICIPATA: compute_exams_data(import_exams(ESTIVA_ANTICIPATA, degree), degree),
        ESTIVA: compute_exams_data(import_exams(ESTIVA, degree), degree),
        AUTUNNALE: compute_exams_data(import_exams(AUTUNNALE, degree), degree)
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
    result_file = SITE_ROOT + f"{get_degree_pathname(degree)}/{SCHOLAR_YEAR}/esami.html"

    template_dir = TEMPLATES_ROOT + "esami/"
    template_file = "table.html"

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render(
        sessioni = [ESTIVA_ANTICIPATA, ESTIVA, AUTUNNALE],
        esami = esami,
        AA = SCHOLAR_YEAR,
        anni =  get_degree_years(degree)
        )
    
    # print( output_from_parsed_template )
    # {% block tabella scoped %}{% endblock %}

    # -- save results
    write_output(output_from_parsed_template, result_file)

if __name__ == '__main__':
    generate_exams(Degree.BACHELOR)
    generate_exams(Degree.MASTER)
    
