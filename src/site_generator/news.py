from jinja2 import Environment, FileSystemLoader
import feedparser
import os
from pprint import pprint

SITE_ROOT = os.environ['SITE_ROOT']
SRC_ROOT = os.environ['SRC_ROOT']
DATA_ROOT = os.environ['DATA_ROOT']
TEMPLATES_ROOT = os.environ['TEMPLATES_ROOT']

def import_news(f_name):
    data = feedparser.parse(f_name)['entries']

    entries = []
    for d in data:
        entries.append({
            'author': d['author'],
            'date': d['published'][5:-3],
            'title': d['title'],
            'body': {
                'type': d['summary_detail']['type'],
                'value': d['summary']
            },
            'links': [
                {'type': l['type'], 'url': l['url']} for l in d['links']
            ]
        })

    pprint( entries )
    return entries

if __name__ == "__main__":
    f_names = [DATA_ROOT + "triennale/20-21/annunci/triennale.xml"]
    result_file = SITE_ROOT + "home/index.html"
    
    template_dir = TEMPLATES_ROOT + "/home/"
    template_file = "news.html"
    
    items = import_news( f_names[0] )

    env = Environment( loader=FileSystemLoader( template_dir ) )
    template = env.get_template( template_file )
    output_from_parsed_template = template.render( items=items )
    
    print( output_from_parsed_template )
    
    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )
