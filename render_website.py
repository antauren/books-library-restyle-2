import json
import os

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

    pages_dir = 'pages'
    os.makedirs(pages_dir, exist_ok=True)

    split_length = 10
    chunked_data = list(more_itertools.chunked(data, split_length))

    for num, page_data in enumerate(chunked_data, start=1):
        page_data_list = list(page_data)
        data_length = len(page_data_list)

        rendered_page = template.render(
            book_groups=more_itertools.chunked(page_data_list,
                                               data_length // 2 + 1 if data_length % 2 else data_length // 2),
        )

        page_path = os.path.join(pages_dir, 'index{}.html'.format(num))
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
    print("Site rebuilded")


rebuild()
server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')
