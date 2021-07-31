from jinja2 import Environment, FileSystemLoader
import feedparser
from pprint import pprint

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

    f_names = ["./bachelor_rss.xml"]
    result_file = "../../home/index.html"
    
    items = import_news( f_names[0] )

    env = Environment( loader=FileSystemLoader(".") )
    template = env.get_template( './news.html' )
    output_from_parsed_template = template.render( items=items )
    
    print( output_from_parsed_template )

    
    # to save the results
    with open(result_file, "w") as fh:
        fh.write( output_from_parsed_template )