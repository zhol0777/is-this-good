import jinja2
from py_markdown_table.markdown_table import markdown_table

import json

import py_markdown_table.markdown_table

def main():
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='scripts'))
    template = environment.get_template('layout.md.jinja')
    with open('scripts/boards.json', 'r', encoding='utf-8') as f:
        board_data = json.load(f)
    nav_order = 1
    for layout_name in board_data.keys():
        choices_per_layout: list[dict] = board_data.get(layout_name)
        if choices_per_layout:
            formatted_choices = []
            multi_line_breaks = { 'name': 0, 'description': 50, 'image': 0, 'links': 0 }
            for choice in choices_per_layout:
                formatted_choices.append({
                    'name': choice['name'],
                    'image': f"![]({choice['image']})",
                    'description': choice['description'],
                    'links': ' '.join([f'[Link]({link})' for link in choice['links']])
                })
                multi_line_breaks['name'] = max(
                    multi_line_breaks['name'],
                    len(formatted_choices[-1]['name']))
                multi_line_breaks['image'] = max(
                    multi_line_breaks['image'],
                    len(formatted_choices[-1]['image']))
                multi_line_breaks['links'] = max(
                    multi_line_breaks['links'],
                    max([len(link) for link in formatted_choices[-1]['links'].split()]))
            content = template.render(
                name=layout_name,
                table=markdown_table(formatted_choices).set_params(
                    row_sep = 'markdown',
                    quote = False,
                    # multiline=multi_line_breaks
                    ).get_markdown(),
                nav_order=nav_order
            )
            with open(f'map/{layout_name}.md', mode='w', encoding='utf-8') as f:
                f.write(content)
                nav_order += 1

main()
