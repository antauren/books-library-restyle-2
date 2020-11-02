import json
import math
import os
from urllib.parse import urljoin

import more_itertools
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def load_json(path):
    with open(path) as fd:
        return json.load(fd)


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    data = load_json(os.path.join('data', 'data.json'))
    for book in data:
        book['img_src'] = os.path.join('..', book['img_src'])
        book['book_path'] = os.path.join('..', book['book_path'])

    pages_dir = 'pages'
    os.makedirs(pages_dir, exist_ok=True)

    split_length = 10
    chunked_data = list(more_itertools.chunked(data, split_length))
    pages_count = math.ceil(len(data) / split_length)

    for num, page_data in enumerate(chunked_data, start=1):
        page_data_list = list(page_data)
        data_length = len(page_data_list)

        rendered_page = template.render(
            book_groups=more_itertools.chunked(page_data_list,
                                               data_length // 2 + 1 if data_length % 2 else data_length // 2),
            pages=[
                {
                    'num': page_num,
                    'url': os.path.join('..', pages_dir, 'index{}.html'.format(page_num))
                }
                for page_num in range(1, pages_count + 1)
            ],
            current_page=num,
            next=num != pages_count,
            previous=num != 1,
            next_url=os.path.join('..', pages_dir, 'index{}.html'.format(num + 1)),
            previous_url=os.path.join('..', pages_dir, 'index{}.html'.format(num - 1))
        )

        page_path = os.path.join(pages_dir, 'index{}.html'.format(num))
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)

        if num == 1:
            page_path = os.path.join(pages_dir, 'index.html')
            with open(page_path, 'w', encoding="utf8") as file:
                file.write(rendered_page)

    print("Site rebuilded")


rebuild()
server = Server()
server.serve(default_filename=os.path.join('pages', 'index1.html'))

server.watch('template.html', rebuild)

server.serve(root='.')
