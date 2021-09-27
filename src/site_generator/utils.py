from header import *

def get_degree_pathname(degree):
    if degree == Degree.BACHELOR:
        return "triennale"
    elif degree == Degree.MASTER:
        return "magistrale"
    else:
        return ""

# -------

def get_degree_years(degree):
    if degree == Degree.BACHELOR:
        return [1, 2, 3]
    elif degree == Degree.MASTER:
        return [1, 2]
    else:
        return []

# -------

def get_days_of_week():
    return ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì']

# -------

def get_course_code_from_name_function(degree):
    """This function returns a function that takes in input a course name
    and gives as output the codename of the course concatenated with
    '.html' if a course with the given name exists, or '#nogo' if it
    doesn't exist.
    
    This function its used in the orari.py for the generation of the schedules.

    """
    
    if degree == Degree.BACHELOR:
        f_name = DATA_ROOT + f"triennale/{SCHOLAR_YEAR}/corsi/corsi.csv"
    elif degree == Degree.MASTER:
        f_name = DATA_ROOT + f"magistrale/{SCHOLAR_YEAR}/corsi/corsi.csv"

    courses_list = read_csv(f_name)

    def get_link(course_name):
        for c in courses_list:
            if course_name.lower() == c['insegnamento'].lower():
                return c['codice'] + ".html"
        return "#nogo"

    # NOTE: here we are returning a function
    return get_link

# -------

def write_output(output, path):
    """This function creates the path and only then saves the output in
    the given path. This is done to avoid OS exceptions like: path not
    found.
    
    Taken from: 
    https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    """

    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            
    with open(path, "w") as f:
        f.write(output)
        
# -------

def read_csv(csv_path):
    try:
        f = open( csv_path )
        result = [ line for line in csv.DictReader(f) ]
        f.close()
        return result
    except FileNotFoundError as e:
        return []
    
