import json
import math
import os
from urllib.parse import urljoin

import more_itertools
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def get_index_filename(num, pages_count, pages_dir):
    if pages_count in {0, pages_count}:
        return ''
    index_file = 'index{}.html'.format(num if num != 1 else '')
    return os.path.join(pages_dir, index_file)


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    json_file = os.path.join('data', 'data.json')
    with open(json_file) as fd:
        data = json.load(fd)
    for book in data:
        book['img_src'] = os.path.join('..', book['img_src'])
        book['book_path'] = os.path.join('..', book['book_path'])

    pages_dir = 'pages'
    os.makedirs(pages_dir, exist_ok=True)
    relative_dir = os.path.join('..', pages_dir)

    split_length = 10
    chunked_data = list(more_itertools.chunked(data, split_length))
    pages_count = math.ceil(len(data) / split_length)

    for num, page_data in enumerate(chunked_data, start=1):
        page_data_list = list(page_data)
        book_groups = more_itertools.chunked(page_data_list,
                                             math.ceil(len(page_data_list) / 2)
                                             )
        pages = [
            {
                'num': page_num,
                'url': get_index_filename(page_num, pages_count, relative_dir)
            }
            for page_num in range(1, pages_count + 1)
        ]
        next_url = get_index_filename(num + 1, pages_count, relative_dir)
        previous_url = get_index_filename(num - 1, pages_count, relative_dir)

        rendered_page = template.render(book_groups=book_groups,
                                        pages=pages,
                                        current_page=num,
                                        next_url=next_url,
                                        previous_url=previous_url
                                        )

        page_path = get_index_filename(num, pages_count, pages_dir)
        if not page_path:
            continue
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilded")


rebuild()
server = Server()
server.serve(default_filename=os.path.join('pages', 'index.html'))

server.watch('template.html', rebuild)

server.serve(root='.')
