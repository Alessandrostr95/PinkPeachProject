#!/usr/bin/python3

'''This code deals with downloading all things related to the official
computer science @ Tor Vergata http://www.informatica.uniroma2.it/.
'''
import datetime
import requests
import os
import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
from enum import Enum
from argparse import ArgumentParser

''' TODOs:
    - Aggiungere flag debug per stampare tutto ciò che scarica lo scraper.

    - Rendere le flags dei parametri più intuitive, specialmente la -d
      per la creazione delle cartelle.

    - Fare in modo che lo scraper crei la struttura delle cartelle da
      solo se si accorge che non sono tutte già presenti.
'''

# ----- Globals -----

DATA_DIR = "../data/"

ERROR_LOG = "../logs/errors_log"

# Used to allow to folders in both italian/english depending on how
# the scraper is instantiated.
IT_DIR_NAMES = {
    "basic_dirs": {
        "courses": "corsi",
        "exams": "esami",
        "news": "annunci",
        "schedule": "orario",
        "teachers": "docenti",
        "graduation": "lauree",
    },
    "special_dirs": {
        "students": "studenti",        
        "bachelor": "triennale",
        "master": "magistrale",
    }
}

ENG_DIR_NAMES = {
    "basic_dirs": {
        "courses": "courses",
        "exams": "exams",
        "news": "news",
        "schedule": "schedule",
        "teachers": "teachers",
        "graduation": "graduation",
    },
    "special_dirs": {
        "students": "students",        
        "bachelor": "bachelor",
        "master": "master",
    }
}


# Used to differentiate between first_name and last_name in case of
# multiple words names.
TEACHERS_NAME = {
    "D'Ambrogio Andrea": {
        "first_name": "Andrea",
        "second_name": "D'Ambrogio",
    },

    "Andrea D'Ambrogio": {
        "first_name": "Andrea",
        "second_name": "D'Ambrogio",
    },    
    
    # --------------
    
    "Di Ianni Miriam": {
        "first_name": "Miriam",
        "second_name": "Di Ianni",
    },

    "Miriam Di Ianni": {
        "first_name": "Miriam",
        "second_name": "Di Ianni",
    },    

    # --------------

    "Zanzotto Fabio Massimo": {
        "first_name": "Fabio Massimo",
        "second_name": "Zanzotto",
    },

    "Fabio Massimo Zanzotto": {
        "first_name": "Fabio Massimo",
        "second_name": "Zanzotto",
    },    

    # --------------
    
    "De Canditiis Daniela": {
        "first_name": "Daniela",
        "second_name": "De Canditiis",
    },

    "Daniela De Canditiis": {
        "first_name": "Daniela",
        "second_name": "De Canditiis",
    },    

    # --------------
    
    "Di Fiore Carmine": {
        "first_name": "Carmine",
        "second_name": "Di Fiore",
    },

    "Carmine Di Fiore": {
        "first_name": "Carmine",
        "second_name": "Di Fiore",
    },    

    # --------------

    "Salsano Stefano Domenico": {
        "first_name": "Stefano Domenico",
        "second_name": "Salsano ",
    },

    "Stefano Domenico Salsano": {
        "first_name": "Stefano Domenico",
        "second_name": "Salsano ",
    },    

    # --------------
    
    "Scalia Tomba Giampaolo": {
        "first_name": "Giampaolo",
        "second_name": "Scalia Tomba",
    },

    "Giampaolo Scalia Tomba": {
        "first_name": "Gimpaolo",
        "second_name": "Scalia Tomba",
    },

    # --------------

    "Giulia Maria Piacentini Cattaneo": {
        "first_name": "Giulia Maria Piacentini",
        "second_name": "Cattaneo"
    },

    "Cattaneo Giulia Maria Piacentini": {
        "first_name": "Giulia Maria Piacentini",
        "second_name": "Cattaneo"        
    },

    # --------------

    "Adriano Di Pasquale": {
        "first_name": "Adriano",
        "second_name": "Di Pasquale",
    },

    "Di Pasquale Adriano": {
        "first_name": "Adriano",
        "second_name": "Di Pasquale",
    },

    # --------------
    
    "Stefano De Luca": {
        "first_name": "Stefano",
        "second_name": "De Luca",
    },

    "De Luca Stefano": {
        "first_name": "Stefano",
        "second_name": "De Luca",        
    },

    # --------------

    "Maria Teresa Pazienza": {
        "first_name": "Maria Teresa",
        "second_name": "Pazienza",
    },

    "Pazienza Maria Teresa": {
        "first_name": "Maria Teresa",
        "second_name": "Pazienza",        
    },

    # --------------

    "Draoli": {
        "first_name": "Draoli",
        "second_name": "",
    }
    
}

# ----- Utils functions -----

def get_current_school_year():
    s = int(str(datetime.datetime.now().year)[2:])
    
    # -- are we past september?
    if datetime.datetime.now().month >= 9:
        scholar_year = str(s) + "-" + str(s + 1)
    else:
        scholar_year = str(s - 1) + "-" + str(s)
    return scholar_year


def log_error(msg):
    timestamp = datetime.datetime.now()
    with open(ERROR_LOG, 'w+') as f:
        f.write(f"{timestamp} - {msg} \n")

# -----------

def parse_command_line_options():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd_name')
    
    # -- subparsers
    bachelor_parser = subparsers.add_parser('bachelor')
    master_parser = subparsers.add_parser('master')

    # -- bachelor arguments
    bachelor_parser.add_argument("-a", "--all", action="store_true", dest="all", help="download all data")
    bachelor_parser.add_argument("-t", "--teachers", action="store_true", dest="teachers", help="download teachers data")
    bachelor_parser.add_argument("-e", "--exams", action="store_true", dest="exams", help="download exams data")
    bachelor_parser.add_argument("-g", "--graduation", action="store_true", dest="graduation", help="download graduation data")
    bachelor_parser.add_argument("-s", "--schedule", action="store_true", dest="schedule", help="download courses schedule data")
    bachelor_parser.add_argument("-n", "--news", action="store_true", dest="news", help="download latest news")

    # TODO: make this more intuitive
    bachelor_parser.add_argument("-d", "--create-dirs", action="store_true", dest="dirs", help="create basic dir structure")
    
    bachelor_parser.add_argument("-c", "--course", dest="course", help="download course data", metavar="COURSE_CODE")
    bachelor_parser.add_argument("-y", "--year", dest="year", help="scholar year in the form 20-21", metavar="SCHOLAR_YEAR")

    # -- master arguments
    master_parser.add_argument("-a", "--all", action="store_true", dest="all", help="download all data")
    master_parser.add_argument("-t", "--teachers", action="store_true", dest="teachers", help="download teachers data")
    master_parser.add_argument("-e", "--exams", action="store_true", dest="exams", help="download exams data")
    master_parser.add_argument("-g", "--graduation", action="store_true", dest="graduation", help="download graduation data")
    master_parser.add_argument("-s", "--schedule", action="store_true", dest="schedule", help="download courses schedule data")
    master_parser.add_argument("-n", "--news", action="store_true", dest="news", help="download latest news")

    # TODO: make this more intuitive
    master_parser.add_argument("-d", "--create-dirs", action="store_true", dest="dirs", help="create basic dir structure")
    
    master_parser.add_argument("-c", "--course", dest="course", help="download course data", metavar="COURSE_CODE")
    master_parser.add_argument("-y", "--year", dest="year", help="scholar year in the form 20-21", metavar="SCHOLAR_YEAR")

    return parser.parse_args()
                
# ---------------------------

class Degree(Enum):
    BACHELOR = 1
    MASTER = 2

class UniScraper(object):

    def __init__(self, degree, data_dir=DATA_DIR, lang="it", create_dir=False):
        """ degree can either be BACHELOR or MASTER"""
        global IT_DIR_NAMES, ENG_DIR_NAMES
        
        self.BASE_URL = "http://www.informatica.uniroma2.it"
        self.degree = degree
        self.data_dir = data_dir

        if lang == "it":
            self.directories = IT_DIR_NAMES
        elif lang == "eng":
            self.directories = ENG_DIR_NAMES
        
        # -- NOTE: assumes code is being run from code folder
        if self.degree == Degree.BACHELOR:
            self.DATA_ROOT = self.data_dir + self.directories['special_dirs']['bachelor']
        elif self.degree == Degree.MASTER:
            self.DATA_ROOT = self.data_dir + self.directories['special_dirs']['master']

        if create_dir:
            self.create_directory_structure()

    # ---------------------------

    def create_directory_structure(self, scholar_year=None):
        """
        Sets up basic directory structure to hold all data.
        """
        dir_name = f"{self.DATA_ROOT}"
        os.makedirs(dir_name, exist_ok=True)

        # TODO: improve this 
        first_year = 2021
        current_year = 2022
            
        for year in range(first_year, current_year):
            # -- create year dir
            scholar_year = str(year)[2:] + "-" + str(year + 1)[2:]            
            dir_name = f"{self.DATA_ROOT}/{scholar_year}"
            os.makedirs(dir_name, exist_ok=True)

            # -- create basic dirs for a given year
            for key in self.directories['basic_dirs']:
                dir_name = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs'][key]}"
                os.makedirs(dir_name, exist_ok=True)

            # -- create dir for every course for a given year
            for course_code in self.get_courses_codes(scholar_year):
                course_dir_name = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['courses']}/{course_code}"
                os.makedirs(course_dir_name, exist_ok=True)

                dir_name = f"{course_dir_name}/{self.directories['basic_dirs']['teachers']}"
                os.makedirs(dir_name, exist_ok=True)

                dir_name = f"{course_dir_name}/{self.directories['special_dirs']['students']}"
                os.makedirs(dir_name, exist_ok=True)

    def __cdl_param(self):
        cdl_param = ""
        # -- compute cdl param for URl
        if self.degree == Degree.BACHELOR:
            cdl_param = "0"
        elif self.degree == Degree.MASTER:
            cdl_param = "1"
        return cdl_param
    
    def __os_param(self, scholar_year):
        if scholar_year:
            return int("20" + get_current_school_year().split("-")[1]) - int("20" + scholar_year.split("-")[1])
        else:
            return "0"  # -- for "current year"

    # ---------------------------

    def get_all_data(self, scholar_year=None):
        """ Downloads all data. If a scholar year is specified, all course data of that given year is downloaded. """
        
        # -- these can only be downloaded for the latest year
        self.get_schedule()
        self.get_exams_schedule()
        self.get_teachers_list()
        self.get_news(scholar_year)
        self.get_graduation_schedule()

        if scholar_year:
            self.get_all_courses_data(scholar_year)
        else:
            first_year = 2001
            current_year = datetime.datetime.now().year
            for year in range(first_year, current_year + 1):
                scholar_year = str(year)[2:] + "-" + str(year + 1)[2:]
                self.get_all_courses_data(scholar_year)
                
    # ---------------------------
    # CODICI CORSO

    def get_courses_codes(self, scholar_year=None):
        """
        Get list of codes for the various courses of the given year.
        """
        if not scholar_year:
            scholar_year = get_current_school_year()
        
        if self.get_courses_list(scholar_year) < 0:
            return []
        else:
            codes = []
            
            file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['courses']}/{self.directories['basic_dirs']['courses']}.csv"
            with open(file_path, "r") as f:
                for line in f.readlines()[1:]:
                    # -- check get_courses_list() to understand format
                    codes.append(line.split(",")[3])
                    
            return codes

    # ---------------------------
    # DATI CORSO PER INTERO ANNO SCOLASTICO

    def get_all_courses_data(self, scholar_year=None):
        """
        Downloads all the data regarding all the course of the specified
        year. If the year is not supplied the current scholar year
        will be used instead.
        """
        # -- compute current scholar year in form 19-20, 20-21
        if not scholar_year:
            scholar_year = get_current_school_year()
        
        codes = self.get_courses_codes(scholar_year)

        # -- for each course get all data
        for code in codes:
            self.get_course_data(code, scholar_year)

    # ---------------------------
    # LISTA CORSI

    def get_courses_list(self, scholar_year=None):
        """
        Scarica la lista dei corsi rispetto ad un particolare anno scolastico.
        scholar_year is given in the format '20-21'.
        """

        if not scholar_year:
            scholar_year = get_current_school_year()
        
        # -- compute URL
        os_param = self.__os_param(scholar_year)
        cdl_param = self.__cdl_param()
        URL_PARAMS = f"/f0?fid=220&srv=4&cdl={cdl_param}&os={os_param}"
        URL = self.BASE_URL + URL_PARAMS
        
        r = requests.get(URL)
        if r.status_code != 200:
            # -- no data available
            warning_msg = f"[(WARNING) {self.degree}]: Couldn't get course list for school_year: [{scholar_year}]"
            log_error(warning_msg)
            exit()

        print(f"[{self.degree}]: Downloading course list for school_year: [{scholar_year}]")

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find("table")
        rows = table.find_all("tr")
        current_year = 0            

        file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['courses']}/{self.directories['basic_dirs']['courses']}.csv"
        with open(file_path, "w+") as out:
            # -- first row with metadata
            out.write("anno,insegnamento,link,codice,settore,CFU,semetre,docente,propedeuticità\n")
            
            # -- skip first row
            for row in rows[1:]:
                if row.find('b'):
                    # -- update year
                    current_year += 1
                else:
                    cols = row.find_all("td")

                    # -- get juicy data
                    anno = str(current_year)        
                    insegnamento = cols[0].a.decode_contents().strip()
                    link = self.BASE_URL + cols[0].a['href'].strip()
                    codice = cols[1].decode_contents().strip()
                    settore = cols[2].decode_contents().strip()
                    cfu = cols[3].decode_contents().strip()
                    semestre = cols[4].decode_contents().strip()
                    docente = cols[5].decode_contents().strip().replace(", ", "-")

                    prop = ""
                    # -- iterate over all preparatory courses
                    for a in cols[6].find_all('a'):
                        prop += a.decode_contents().strip() + "-"

                    out.write(f"{anno},{insegnamento},{link},{codice},{settore},{cfu},{semestre},{docente},{prop}\n")
        return 0

    # ---------------------------
    # DATI CORSO
    
    def get_course_data(self, course_code, scholar_year=None, download=False):
        """Downloads all the data regarding the course identified by the
        {courseCode} value. 

        If the year is not supplied the current scholar year will be used instead. 

        When download is set to True, all the material will be
        downloaded in the proper folder. If instead it is set to
        False, only the links will be downloaded.

        """
        os_param = self.__os_param(scholar_year)
        URL_PARAMS = f"/f0?fid=220&srv=0&os={os_param}&id={course_code}"
        URL = self.BASE_URL + URL_PARAMS

        # -- compute current scholar year in form 19-20, 20-21
        if not scholar_year:
            s = int(str(datetime.datetime.now().year)[2:])
            scholar_year = str(s - 1) + "-" + str(s)        
        
        r = requests.get(URL)
        if r.status_code != 200:
            # -- no data available
            warning_msg = f"[(WARNING) {self.degree}, {scholar_year}]: Could not download course data for course: [{course_code}]"
            print(warning_msg)
            log_error(warning_msg)
            exit()

        print(f"[{self.degree}, {scholar_year}]: Downloading course data for course: [{course_code}]")

        output = {}
        soup = BeautifulSoup(r.text, 'html.parser')

        basic_info_table = soup.find("h2", string="Informazioni").findNext("table")
        communications_table = soup.find("h2", string="Comunicazioni").findNext("table")
        lectures_table = soup.find("h2", string="Lezioni").findNext("table")
        materials_table = soup.find("h2", string="Materiale didattico").findNext("table")
        programma_table = soup.find("h2", string="Programma").findNext("table")
        testi_table = soup.find("h2", string="Testi di riferimento").findNext("table")
        ricevimento_table = soup.find("h2", string="Ricevimento studenti").findNext("table")
        esame_table = soup.find("h2", string="Modalità di esame").findNext("table")
        
        # -- extract data
        nome_corso = soup.find("title").decode_contents().strip()
        docente = soup.find("span", {"id": "docNome"}).decode_contents().strip()
        output["nomeCorso"] = nome_corso
        output["docente"] = self.__extract_course_teacher_name(docente)
        
        output = self.__get_course_basic_info(output, basic_info_table)
        output = self.__get_course_communication(output, communications_table)
        output = self.__get_course_lectures(output, lectures_table)
        output = self.__get_course_materials(output, materials_table)

        if download:
            self.__download_course_materials(course_code, scholar_year, output["materiale"])
        
        output["programma"] = str(programma_table)
        output["testiRiferimento"] = str(testi_table)
        output["ricevimento"] = str(ricevimento_table)
        output["modalitàEsame"] = str(esame_table)

        # -- write output json
        file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['courses']}/{course_code}/{course_code}.json"
        with open(file_path, "w+") as out:
            json.dump(output, out, indent=2)

    # ---------

    def __extract_course_teacher_name(self, text):
        names = text.split(",")
        res = []

        for name in names:
            name = name.strip()
            
            res_name = {}
            name_words = name.replace("'", " ").split()
            if len(name_words) == 2:
                # -- traditional name
                res_name["first_name"] = name_words[0]
                res_name["second_name"] = name_words[1]
            else:
                # -- special name, use dict
                res_name["first_name"] = TEACHERS_NAME[name]["first_name"]
                res_name["second_name"] = TEACHERS_NAME[name]["second_name"]
                    
            res.append(res_name)
                    
        return res

    # ---------

    # https://stackoverflow.com/questions/54265391/find-all-end-nodes-that-contain-text-using-beautifulsoup4
    def __extract_all_text_from_soup(self, obj):
        """ Recursively extract all text from a beautifulSoup object """
        if isinstance(obj, NavigableString):
            return obj
        else:
            res = ""
            for child in obj:
                res += self.__extract_all_text_from_soup(child)
            return res.strip()
    
    def __get_course_basic_info(self, output, basic_table):
        info_rows = basic_table.find_all("tr")
        
        anno_accademico = info_rows[0].td.decode_contents().strip()
        crediti = info_rows[1].td.decode_contents().strip()
        settore = info_rows[2].td.decode_contents().strip()
        anno = info_rows[3].td.decode_contents().strip()
        semestre = info_rows[4].td.decode_contents().strip()
        propedeuticità = info_rows[5].td.decode_contents().strip()

        # -- write basic info to JSON object
        output["annoAccademico"] = anno_accademico
        output["crediti"] = crediti
        output["settore"] = settore
        output["anno"] = anno
        output["semestre"] = semestre
        output["propedeuticità"] = propedeuticità

        return output

    def __get_course_communication(self, output, communications_table):
        communication_rows = communications_table.find_all("tr", recursive=False)
        comms = []
        for row in communication_rows:
            # -- scrape single communication
            communication = {}
            communication["titolo"] = row.find("h3").decode_contents().strip()
            communication["data"] = row.find("span", {"id": "data"}).decode_contents().strip()
            communication["contenuto"] = row.td.decode_contents().strip()
            # -- remove repeated title+data
            i = communication["contenuto"].find("<br/>") + len("<br/>")
            communication["contenuto"] = communication["contenuto"][i:]
            comms.append(communication)
            
        output["comunicazioni"] = comms
        return output


    # <tr><td><span id="lezId">6</span> </td> <td> <span id="data">23-10-2020</span><br/>
    
    def __get_course_lectures(self, output, lectures_table):
        lecture_rows = lectures_table.find_all("tr", recursive=False)
        lects = []
        for row in lecture_rows:
            lecture = {}
            lecture["id"] = row.find("span", {"id": "lezId"}).decode_contents().strip()
            lecture["data"] = row.find("span", {"id": "data"}).decode_contents().strip()
            lecture["contenuto"] = row.find_all("td")[1].decode_contents().strip()
            # -- remove repeated id+data
            i = lecture["contenuto"].find("<br/>") + len("<br/>")
            lecture["contenuto"] = lecture["contenuto"][i:]
            lects.append(lecture)
        output["lezioni"] = lects
        return output

    def __get_course_materials(self, output, materials_table):
        material_rows = materials_table.find_all("tr", recursive=False)
        mats = []
        for row in material_rows:
            cols = row.find_all("td")

            # -- needed for dataUpload and dimensione
            i = cols[1].a['title'].find("Data: ") + len("Data: ")
            j = cols[1].a['title'].find("Dimensione: ")
            k = j + len("Dimensione: ")

            materiale = {}
            # -- sometimes title is not inside <p></p> but directly in <td></td>
            if cols[0].find("p"):
                materiale["titolo"] = cols[0].p.decode_contents().strip()
            else:
                materiale["titolo"] = cols[0].decode_contents().strip()
            
            materiale["dataUpload"] = cols[1].a['title'][i:j].strip()
            materiale["link"] = self.BASE_URL + cols[1].a['href'].strip()
            materiale["dimensione"] = cols[1].a['title'][k:].strip()
            mats.append(materiale)

        output["materiale"] = mats
        return output

    def __download_course_materials(self, course_code, scholar_year, material):
        for m in material:
            print(f"[{self.degree}, {scholar_year}, {course_code}]: Downloading [{m['link']}]")

            r = requests.get(m["link"], allow_redirects=True)
            
            filename = m["link"].split("/")[-1].replace(" ", "-")
            outFile = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['courses']}/{course_code}/{self.directories['basic_dirs']['teachers']}/{filename}"
            # -- NOTE: get ext from Content-Type?
            # outFile = outFile + r.headers.get('content-type').replace("/", ".")
            with open(outFile, 'wb+') as f:
                f.write(r.content)

    # ---------------------------
    # LISTA DOCENTI
        
    def get_teachers_list(self):
        """
        Scarica le informazioni riguardanti i professori.
        """

        # -- compute URL
        cdl_param = self.__cdl_param()
        URL_PARAMS = f"/f0?fid=30&srv=4&cdl={cdl_param}"
        URL = self.BASE_URL + URL_PARAMS

        r = requests.get(URL)
        if r.status_code != 200:
            warning_msg = f"[(WARNING) {self.degree}]: Could not download teachers data"
            print(warning_msg)
            log_error(warning_msg)
            exit()

        print(f"[{self.degree}]: Downloading teachers data")            

        # -- compute current scholar year in form 19-20, 20-21
        scholar_year = get_current_school_year()

        file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['teachers']}/{self.directories['basic_dirs']['teachers']}.csv"
        with open(file_path, "w+") as out:
            # -- first row with metadata
            out.write("nome,qualifica,studio,telefono,mail,homepage,insegnamenti\n")
            
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find("table")
            rows = table.find_all("tr")

            for row in rows[1:]:
                cols = row.find_all("td")

                nome = cols[0].a.decode_contents().strip()
                qualifica = cols[1].decode_contents().strip()
                studio = cols[2].decode_contents().strip()
                telefono = cols[3].decode_contents().strip()

                mail = cols[4].a.img['title'].strip() if cols[4].find("a") else ""
                homepage = cols[5].a['href'].strip() if cols[5].find("a") else ""
                # cv = ""
                insegnamenti = ""
                for ins in cols[7].find_all("a"):
                    insegnamenti += ins.decode_contents().strip() + "-"
                insegnamenti = insegnamenti[:-1]
                out.write(f"{nome},{qualifica},{studio},{telefono},{mail},{homepage},{insegnamenti}\n")

    # ---------------------------
    # ORARIO LEZIONI

    def get_schedule(self):
        """
        Scarica le informazioni riguardanti gli orari delle lezioni.
        """

        URL_PARAMS = ""
        if self.degree == Degree.BACHELOR:
            URL_PARAMS = "/pages/trien/orario/orario.htm"
        elif self.degree == Degree.MASTER:
            URL_PARAMS = "/pages/magis/orario/orario.htm"            
        URL = self.BASE_URL + URL_PARAMS

        r = requests.get(URL)
        if r.status_code != 200:
            warning_msg = f"[(WARNING) {self.degree}]: Could not download schedule data"
            log_error(warning_msg)
            print(warning_msg)
            exit()

        print(f"[{self.degree}]: Downloading schedule data")

        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find("h1").decode_contents().strip()

        # -- compute current sem
        semester = ""
        if "primo" in title:
            semester = "1"
        elif "secondo" in title:
            semester = "2"

        # -- compute current year
        scholar_year = get_current_school_year()

        file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['schedule']}/sem{semester}.csv"

        with open(file_path, "w+") as out:
            # -- first row with metadata
            out.write("anno,ora,lunedì,martedì,mercoledì,giovedì,venerdì\n")
            
            table = soup.find("table")
            rows = table.find_all("tr")
            current_year = 0
            skip = False
            default_room = ""

            for row in rows:
                if skip:
                    # -- skip current row
                    skip = False
                    continue

                if row.find("h2"):
                    current_year += 1
                    # -- skip next row
                    skip = True
                    # -- get default room for current year
                    s = row.b.decode_contents().strip()
                    default_room = s[s.find("Lezioni in aula") + len("Lezioni in aula"):].split()[0]
                    
                else:
                    # -- get juicy data
                    cols = row.find_all("td")
                    hour = cols[0].decode_contents().strip()

                    # -- schedule[i] := course + room of i-th day of
                    # -- the week for a specified hour.
                    schedule = []
                    for i in range(1, 6):
                        if cols[i].find("a"):
                            course = cols[i].a.decode_contents().strip()
                            room = cols[i].span.decode_contents().strip()

                            if room == "()":
                                room = "(" + default_room + ")"
                            
                            schedule.append(course + room)
                        else:
                            schedule.append("X")
                            
                    out.write(f"{current_year},{hour}, {schedule[0]},{schedule[1]},{schedule[2]},{schedule[3]},{schedule[4]}\n")
        
    # ---------------------------
    # ESAMI

    # TODO: make sure the exam section makes sense with respect to
    # scholar_year
    def get_exams_schedule(self):
        """
        Scarica le informazioni riguardanti le date degli esami rispetto a
        tutte le sessioni possibili per il corrente anno scolastico.
        """
        # -- this actually refers to previous scholar year
        self.__get_exams_by_session("invernale")
        # -- these to current one
        self.__get_exams_by_session("estiva-anticipata")
        self.__get_exams_by_session("estiva")
        self.__get_exams_by_session("autunnale")
            
    def __get_exams_by_session(self, session):
        """        
        Scarica le informazioni riguardanti le date degli esami dei vari
        appelli rispetto ad una specificata sessione, che può essere
        una tra: INVERNALE, ESTIVA-ANTICIPATA, ESTIVA, AUTUNNALE. 
        
        NOTE: La session INVERNALE fa riferimento al precedente anno scolastico.
        """
        if session not in ["invernale", "estiva-anticipata", "estiva", "autunnale"]:
            # -- unknown session
            print(f"[(ERROR) {self.degree}]: Uknown session value {session}. Valid values are: [invernale, estiva anticipata, estiva, autunnale]")
            exit()

        # -- compute year and URL
        s = int(str(datetime.datetime.now().year)[2:])
        url_base = f"/pages/{'trien' if self.degree == Degree.BACHELOR else 'magis'}/esami/"
        if session == "invernale":
            # -- this belongs to previous year
            s = int(str(datetime.datetime.now().year - 1)[2:])
            URL_PARAMS = url_base + "dateEsami0.htm"
        elif session == "estiva-anticipata":
            URL_PARAMS = url_base + "dateEsami1.htm"
        elif session == "estiva":
            URL_PARAMS = url_base + "dateEsami3.htm"
        elif session == "autunnale":
            URL_PARAMS = url_base + "dateEsami5.htm"            
        year = str(s - 1) + "-" + str(s)

        URL = self.BASE_URL + URL_PARAMS
        file_path = f"{self.DATA_ROOT}/{year}/{self.directories['basic_dirs']['exams']}/{self.directories['basic_dirs']['exams']}-{session}.csv"
        self.__get_exams_data(URL, file_path)
    
    def __get_exams_data(self, url, outfile):
        """        
        Scarica le informazioni riguardanti le date degli esami dei vari
        appelli a partire da un URL. Salva il contenuto sul file specificato.
        """        
        r = requests.get(url)
        if r.status_code != 200:
            warning_msg = f"[(WARNING) {self.degree}]: Coud not download exam list: [{url}]"
            log_error(warnings_msg)
            print(warning_msg)
            exit()

        print(f"[{self.degree}]: Downloading exam list: [{url}]")
            
        with open(outfile, "w+") as out:
            # -- first row with metadata
            out.write("appello,anno,insegnamento,docente,scritto_data,scritto_ora,scritto_aula,orale_data,orale_ora,orale_aula\n")
            soup = BeautifulSoup(r.text, 'html.parser')
            tables = soup.find_all("table")

            for appello in [1, 2]:
                rows = tables[appello - 1].find_all("tr")
                current_year = 0
                for row in rows[2:]:
                    if row.find("b"):
                        current_year += 1
                    else:
                        cols = row.find_all("td")

                        # -- get juicy data
                        insegnamento = cols[0].a.decode_contents().strip()
                        docente = cols[1].decode_contents().strip().replace(", ", "-")
                        scritto_data = cols[2].decode_contents().strip()
                        scritto_ora = cols[3].decode_contents().strip()
                        scritto_aula = cols[4].decode_contents().strip()
                        orale_data = cols[5].decode_contents().strip()
                        orale_ora = cols[6].decode_contents().strip()
                        orale_aula = cols[7].decode_contents().strip()
                        out.write(f"{appello},{current_year},{insegnamento},{docente},{scritto_data},{scritto_ora},{scritto_aula},{orale_data},{orale_ora},{orale_aula}\n")

    # ---------------------------
    # SEDUTE DI LAUREA

    def get_graduation_schedule(self):
        # -- compute current year
        scholar_year = get_current_school_year()
        
        URL_PARAMS = ""
        if self.degree == Degree.BACHELOR:
            URL_PARAMS = "/pages/trien/lauree/dateLauree.htm"
        elif self.degree == Degree.MASTER:
            URL_PARAMS = "/pages/magis/lauree/dateLauree.htm"            
        URL = self.BASE_URL + URL_PARAMS
        
        r = requests.get(URL)
        if r.status_code != 200:
            warning_msg = f"[(WARNING) {self.degree}]: Coud not download graduation schedule: [{URL}]"
            log_error(warning_msg)
            print(warning_msg)
            exit()

        print(f"[{self.degree}]: Downloaded graduation schedule : [{URL}]")

        output = []
        soup = BeautifulSoup(r.text, 'html.parser')
        # table = soup.find("table")
        rows = soup.find_all("tr")
        
        for row in rows:
            if "Data" in row.decode_contents():
                continue

            cols = row.find_all("td")

            # -- extract juciy data
            rowData = {}
            rowData["giorno"] = cols[0].text.strip()
            rowData["sessione"] = cols[1].text.strip()
            rowData["aa"] = cols[2].text.strip()

            output.append(rowData)

        # -- write output json
        file_path = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['graduation']}/{self.directories['basic_dirs']['graduation']}.json"
        with open(file_path, "w+") as out:
            json.dump(output, out, indent=2)
    
    # ---------------------------
    # NEWS

    def __create_rss_feed(self):
        if self.degree == Degree.BACHELOR:
            degree = "Bachelor"
            rss_file = f"{self.directories['special_dirs']['bachelor']}.xml"
        elif self.degree == Degree.MASTER:
            degree = "Master"
            rss_file = f"{self.directories['special_dirs']['master']}.xml"

        rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
      <title>Computer Science, {degree}'s Degree News @ Tor Vergata</title>
      <link> http://www.informatica.uniroma2.it </link>
      <description>News for {degree} degree CS @ Tor Vergata</description>
       <!-- Items go here -->

      
  </channel>
</rss>
"""        
        scholar_year = get_current_school_year()
        filename = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['news']}/{rss_file}"

        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(rss_feed)

    def __create_rss_entry(self, entry):
        title, date, author, description, enclosure = self.__extract_news_data(entry)
        # NOTE: correct whitespaces here are crucial to be able to
        # understand if a news was already added in
        # __update_rss_feed()
        rss_entry = (
             "    <item>\n"
            f"      <title>{title}</title>\n"
            f"      <author>{author}</author>\n"
            f"      <pubDate>{date}</pubDate>\n"
            f'      <enclosure url="{enclosure}" type="application/pdf" />\n'
            f"      <description>\n"
            f"        <![CDATA[{description}\n"
            f"        ]]></description>\n"
             "    </item>\n\n")
        return rss_entry

    def __extract_news_data(self, entry):
        header = str(entry.th)

        # get title
        title = header[header.find("\"/>") + 4:header.find("<br/>")]

        # get date
        date = header[header.find("gray;\">        ") + len("gray;\">        "):header.find("inviato")].split(" ")
        dmy = date[0].split("-")
        hm = date[1].split(":")
        day, month, year = int(dmy[0]), int(dmy[1]), int(dmy[2])
        hour, minute = int(hm[0]), int(hm[1])
        date = datetime.datetime(year, month, day, hour, minute).strftime("%a, %d %b %Y %H:%M:%S %z")

        # get author
        author = header[header.find("inviato da ") + len("inviato da "): header.find("</span></th>")]

        # get description
        description = entry.select_one("tr:nth-of-type(2)").text.replace("\n", "<br />")
        enclosure = ""

        # -- deal with links
        links = entry.select_one("tr:nth-of-type(2)").find_all("a")
        for link in links:
            # in case of remote urls <a href="..."> text </a>
            if "http" in link.get("href"):
                description = description.replace(link.text, link.get("href"))
            else:
                enclosure = self.BASE_URL + link.get("href")

        return title, date, author, description, enclosure

    def __update_rss_feed(self, rss_entries, scholar_year=None):
        # -- compute filename
        if not scholar_year:
            scholar_year = get_current_school_year()

        if self.degree == Degree.BACHELOR:
            rss_file = f"{self.directories['special_dirs']['bachelor']}.xml"
        elif self.degree == Degree.MASTER:
            rss_file = f"{self.directories['special_dirs']['master']}.xml"        
        
        filename = f"{self.DATA_ROOT}/{scholar_year}/{self.directories['basic_dirs']['news']}/{rss_file}"

        # if the file does not exist, create it with initial content
        if not os.path.isfile(filename):
            self.__create_rss_feed()
        
        # -- read previous news
        rss_file = open(filename, 'r', encoding='utf-8')
        contents = rss_file.readlines()
        rss_file.close()

        # -- modify content accordingly
        for rss_entry in rss_entries:
            # NOTE: this checks only works if the rss entry was
            # created with the right spaces in __create_rss_entry()
            if "".join(contents).find(rss_entry) == -1:
                contents.insert(8, rss_entry)

        # -- write updates
        rss_file = open(filename, 'w+', encoding='utf-8')
        rss_file.writelines(contents)
        rss_file.close()

    def get_news(self, scholar_year=None):
        # -- compute URL
        cdl_param = self.__cdl_param()
        URL_PARAMS = f"/f0?fid=50&srv=4&cdl={cdl_param}&pag=0"
        URL = self.BASE_URL + URL_PARAMS
        
        r = requests.get(URL)
        if r.status_code != 200:
            warning_msg = f"[(WARNING) {self.degree}]: Coud not download latest news"
            log_error(warning_msg)
            print(warning_msg)
            exit()
            
        print(f"[{self.degree}]: Downloading latest news")

        soup = BeautifulSoup(r.text, 'html.parser')
        entries = soup.find_all("table")
        entries.reverse()
        
        rss_entries = []
        for entry in entries:
            rss_entries.append(self.__create_rss_entry(entry))

        self.__update_rss_feed(rss_entries, scholar_year)

# -------------------------------------------------------

if __name__ == "__main__":
    args = parse_command_line_options()
    
    scraper = None
    if args.cmd_name == "bachelor":
        scraper = UniScraper(Degree.BACHELOR)
    elif args.cmd_name == "master":
        scraper = UniScraper(Degree.MASTER)
    else:
        print("[ERROR]: Scraper only works in two modes: {bachelor, master}!")
        exit()

    scholar_year = args.year if args.year else None
    all_mode = args.all
    dirs_mode = args.dirs
    teacher_mode = args.teachers
    exam_mode = args.exams
    schedule_mode = args.schedule
    graduation_mode = args.graduation
    news_mode = args.news
    course_mode = True if args.course else False
    course = args.course

    if dirs_mode:
        scraper.create_directory_structure(scholar_year)

    # -- all mode overwrites everything else
    if all_mode:
        scraper.get_all_data(scholar_year)
        exit()

    if graduation_mode:
        scraper.get_graduation_schedule()        

    if teacher_mode:
        scraper.get_teachers_list()

    if exam_mode:
        scraper.get_exams_schedule()

    if news_mode:
        scraper.get_news(scholar_year)

    if course_mode:
        scraper.get_course_data(course, scholar_year)

# -------------------------------------------------------
# Example Usage

# scarica tutti i dati della triennale per l'anno 20-21
# python3 scraper.py bachelor -a -y 20-21

# scarica tutti i dati della triennale per l'anno 20-21
# python3 scraper.py bachelor -a -y 20-21

# scarica tutti i dati della triennale per l'anno 20-21
# python3 scraper.py bachelor -a -y 20-21

# scarica tutti i dati della triennale per l'anno 20-21
# python3 scraper.py bachelor -a -y 20-21


# for debugging
# print("year: " + str(scholar_year))
# print("all_mode: " + str(all_mode))
# print("teacher_mode: " + str(teacher_mode))
# print("exam_mode: " + str(exam_mode))
# print("schedule_mode: " + str(schedule_mode))
# print("news_mode: " + str(news_mode))
# print("course_mode: " + str(course_mode))
# print("course: " + str(course))
