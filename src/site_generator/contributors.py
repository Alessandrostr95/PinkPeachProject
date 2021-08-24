from jinja2 import Environment, FileSystemLoader
import requests
import json
from pprint import pprint
import os

SITE_ROOT = os.environ['SITE_ROOT'] if "SITE_ROOT" in os.environ else "../../site/"
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT'] if "TEMPLATES_ROOT" in os.environ else "../../templates/"
DATA_ROOT = os.environ['DATA_ROOT'] if "DATA_ROOT" in os.environ else "../../data/"
SRC_ROOT = os.environ['SRC_ROOT'] if "SRC_ROOT" in os.environ else "../../src/"

# Utilizzato da modify_contributors_with_custom_data() per cambiare le
# informazioni scaricate da github con dati a piacere.
CUSTOM_DATA = {
    "LeonardoE95": {
        "login": "Leonardo Tamiano",
        "html_url": "https://leonardotamiano.xyz",
    }
}

def download_github_avatars(contributors):
    for user in contributors:
        img = requests.get( user['avatar_url'] )
        with open(f"{SITE_ROOT}assets/contributors/{user['login']}.jpg", "wb") as f:
            f.write( img.content )

def download_github_contrib_data():
    url = "https://api.github.com/repos/Alessandrostr95/PinkPeachProject/contributors"
    resp = requests.get( url )
    data = json.loads( json.dumps( resp.json() ) )
    return data

def write_github_contrib_data( contributors ):
    data = []

    for user in contributors:        
        data.append({
            'username': user['login'],
            'img_url': f"{SITE_ROOT}assets/contributors/{user['login']}.jpg",
            'git_url': user['html_url'],
            'contributions': user['contributions']
        })

    #pprint( json.dumps(data, indent=True) )
    
    with open(f"{SITE_ROOT}assets/js/contributors-data.json", "w") as f:
        f.write( json.dumps(data, indent=True) )

def modify_contributors_with_custom_data ( contributors ):
    """Funzione che modifica i dati scaricati da github per cambiare
    link/username ed eventuale immagine di profilo."""

    for user in contributors:
        user['login.bkp'] = user['login'] # -- save in case of changes
        if user['login.bkp'] in CUSTOM_DATA:
            for field in CUSTOM_DATA[user['login.bkp']]:
                user[field] = CUSTOM_DATA[user['login.bkp']][field]

# -----------------------------------------

def write_contributors( contributors ):
    result_file = SITE_ROOT + "home/informazioni.html"
    
    template_dir = TEMPLATES_ROOT + "/home/"
    template_file = "informazioni.html"

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( contributors=contributors )
    
    # print( output_from_parsed_template )
    
    # to save the results
    with open(result_file, "w") as fh:
         fh.write( output_from_parsed_template )

if __name__ == '__main__':
    contributors = download_github_contrib_data()
    download_github_avatars( contributors )
    modify_contributors_with_custom_data( contributors )
    # write_github_contrib_data( contributors ) questo al momento non server
    write_contributors( contributors )
