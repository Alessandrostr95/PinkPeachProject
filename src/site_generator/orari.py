# -- general imports
from header import DATA_ROOT
from header import TEMPLATES_ROOT
from header import SITE_ROOT
from header import SCHOLAR_YEAR

from header import Degree

# -- import all other libraries imported in header
from header import *

from utils import get_degree_pathname
from utils import get_degree_years
from utils import get_days_of_week
from utils import get_course_code_from_name_function
from utils import write_output
from utils import read_csv

# ------------------------------
# funzioni helpers

def csv2json(f_name, degree):
    """
    Funzione che legge il csv degli orari ottenuto con scraper.py e
    ritorna un dizionario con una struttura JSON oriented
    """

    lines = read_csv(f_name)

    years = get_degree_years(degree)
    days = get_days_of_week()
    get_link = get_course_code_from_name_function(degree)

    data = {}
    for y in years:
        data[y] = {}
        for d in days:
            data[y][d] = {}
    
    for line in lines:
        anno = int(line["anno"])
        ora = int(line["ora"].split(":")[0])
        for d in days:
            materia = line[d].strip().replace("(","<br />(")
            data[anno][d][ora] = {
                "entry": materia if materia != "X" else "",
                "link": get_link(line[d].strip().split("(")[0])
            }
    
    return data

# ------------------------------

def generate_schedule(degree):
    global DATA_ROOT, SITE_ROOT
    
    # TODO: here we have to decide whether we are using sem1.csv or sem2.csv
    csv_file = DATA_ROOT + f"{get_degree_pathname(degree)}/{SCHOLAR_YEAR}/orario/sem1.csv"
    result_file = SITE_ROOT + f"{get_degree_pathname(degree)}/{SCHOLAR_YEAR}/orario.html"

    template_dir = TEMPLATES_ROOT + "orario/"
    template_file = "table.html"

    data = csv2json(csv_file, degree)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    output_from_parsed_template = template.render(
        orari=data,
        H=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    )

    # -- save results
    write_output(output_from_parsed_template, result_file)

if __name__ == "__main__":
    generate_schedule(Degree.BACHELOR)
    generate_schedule(Degree.MASTER)

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
