"""给elementui tree的label增加章节标题"""
from typing import List


NUMBER_OF_LEVEL_ITEM = 10

HEADING_LEVEL = {
    1: [f'{i + 1}' for i in range(NUMBER_OF_LEVEL_ITEM)],
    2: [f'.{i + 1}' for i in range(NUMBER_OF_LEVEL_ITEM)],
    3: [f'.{chr(ord("a") + i)}' for i in range(NUMBER_OF_LEVEL_ITEM)],
}


def add_section_number(node_list: List, heading_level: int, prefix: str = ''):
    for i, node in enumerate(node_list):
        new_prefix = f'{prefix}{HEADING_LEVEL[heading_level][i]}'
        node['label'] = f'{new_prefix} {node["label"]}'
        add_section_number(node['children'], heading_level + 1, new_prefix)
