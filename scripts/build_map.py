import jinja2

import json

def main():
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='scripts'))
    template = environment.get_template('layout.md.jinja')
    with open('scripts/boards.json', 'r', encoding='utf-8') as f:
        board_data = json.load(f)
    for layout_name in board_data.keys():
        choices_per_layout: list[dict] = board_data.get(layout_name)
        if choices_per_layout:
            content = template.render(
                name=layout_name,
                choices_per_layout=choices_per_layout
            )
            with open(f'map/{layout_name}.md', mode='w', encoding='utf-8') as f:
                f.write(content)

main()
