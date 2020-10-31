import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_json(path):
    with open(path) as fd:
        return json.load(fd)


data = load_json('downloads/data.json')

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

rendered_page = template.render(
    books=data,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
