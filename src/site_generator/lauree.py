# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

# -- import all libraries importer in header
from header import *

# ------------------------------

def import_lauree(triennale=True):
    """
        Data una sessione, legge il file csv degli esami e ritorna una lista di oggetti 'riga'
    """
    cdl = "triennale" if triennale else "magistrale"
    f_name = DATA_ROOT + f"{cdl}/{SCHOLAR_YEAR}/lauree/lauree.json"
    
    f = open(f_name, "r")
    lauree = json.load(f)
    f.close()
    
    return lauree
    
def write_lauree(triennale=True):
    # pprint( esami )
    date_lauree = import_lauree(triennale=triennale)
    
    cdl = "triennale" if triennale else "magistrale"
    result_file = SITE_ROOT + f"{cdl}/{SCHOLAR_YEAR}/lauree.html"

    template_dir = TEMPLATES_ROOT + "lauree/"
    template_file = "base.html"

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( date_lauree = date_lauree )
    
    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )

if __name__ == '__main__':
    write_lauree()
    write_lauree(False)
