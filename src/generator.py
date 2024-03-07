import os
from pathlib import Path

from textnode import (
    BlockTypes,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if block_to_block_type(blocks[0]) != BlockTypes.block_type_heading.value[0]:
        raise Exception("Page must have a heading. An h1.")
    return blocks[0].split("#")[1].strip()


def generate_page(from_path, template_path, dest_path):
    print(
        f"""Generating page from {from_path} to {
            dest_path} using {template_path}..."""
    )

    markdown = []
    template = []
    with open(f"{from_path}", "r") as md:
        markdown = md.read()

    with open(f"{template_path}", "r") as tmpl:
        template = tmpl.readlines()

    nodes = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    with open(f"{dest_path}", "w+") as html:
        new_t = ""
        for t in template:
            if "{{ Title }}" in t:
                new_t = t.replace("{{ Title }}", title)
                html.write(new_t)
                continue
            if "{{ Content }}" in t:
                new_t = t.replace("{{ Content }}", nodes)
                html.write(new_t)
                continue
            html.write(t)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    md_list = []
    for root, _, f_names in os.walk(dir_path_content):
        for f in f_names:
            md_list.append(os.path.join(root, f))
    for md in md_list:
        print(
            f"""Generating page from {md} to {
                dest_dir_path} using {template_path}..."""
        )

        markdown = ""
        template = []
        with open(f"{md}", "r") as md:
            markdown = md.read()

        with open(f"{template_path}", "r") as tmpl:
            template = tmpl.readlines()

        nodes = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

        print(f"MD => {md.name.replace('md', 'html')}")

        dest_path = f"""{dest_dir_path}{os.path.dirname(md.name.replace(
            'content/', ''))}"""
        if not Path(dest_path).exists():
            os.makedirs(dest_path)
        with open(
            f"""{
                dest_dir_path}{md.name.replace("content/", "").replace('md', 'html')}""",
            "w+",
        ) as html:
            new_t = ""
            for t in template:
                if "{{ Title }}" in t:
                    new_t = t.replace("{{ Title }}", title)
                    html.write(new_t)
                    continue
                if "{{ Content }}" in t:
                    new_t = t.replace("{{ Content }}", nodes)
                    html.write(new_t)
                    continue
                html.write(t)
