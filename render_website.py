import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import more_itertools


def load_json(path):
    with open(path) as fd:
        return json.load(fd)


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    data = load_json('downloads/data.json')
    group_1, group_2 = more_itertools.distribute(2, data)
    rendered_page = template.render(
        book_groups=[group_1, group_2],
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilded")


rebuild()
server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')