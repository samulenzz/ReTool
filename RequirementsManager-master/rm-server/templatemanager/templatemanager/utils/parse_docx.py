import json
import time
from typing import List
from dataclasses import dataclass, field

from docx import Document


# @dataclass
# class DocxSection:
#     heading_level: int = None
#     title: str = ''
#     text: str = ''
#     sub_sections: List = field(default_factory=list)
#
#
# def parse_docx(docx_path: str) -> DocxSection:
#     docx = Document(docx_path)
#     paragraphs = list(docx.paragraphs)
#     # 初始化堆栈
#     stack = []
#     # 填入根节点
#     stack.append(
#         DocxSection(heading_level=0, title='ROOT')
#     )
#     # 开始遍历
#     for paragraph in paragraphs:
#         if paragraph.style.name in HEADING_LEVEL:
#             current_heading_level = HEADING_LEVEL.get(paragraph.style.name)
#             # 如果当前heading_level大于等于栈顶heading_level，直接进栈
#             if current_heading_level >= stack[-1].heading_level:
#                 tmp_docx_section = DocxSection(
#                     heading_level=current_heading_level,
#                     title=paragraph.text
#                 )
#                 stack.append(tmp_docx_section)
#             # 否则，栈顶元素依次出栈
#             tmp_docx_sections = []
#             while True:
#                 if len(stack) < 2:
#                     break
#                 tmp_docx_section = stack.pop()
#                 tmp_docx_sections.append(tmp_docx_section)
#                 if tmp_docx_section.heading_level > stack[-1].heading_level:
#                     stack[-1].sub_sections = tmp_docx_sections[::-1]
#                     tmp_docx_sections = []
#                 # 再次将current_heading_level与栈顶元素比较
#                 if current_heading_level >= stack[-1].heading_level:
#                     tmp_docx_section = DocxSection(
#                         heading_level=current_heading_level,
#                         title=paragraph.text
#                     )
#                     stack.append(tmp_docx_section)
#                     break
#         # 否则，直接将文本附加至栈顶节点
#         else:
#             stack[-1].text += paragraph.text + '\n'
#
#     # 将栈内剩余元素出栈
#     tmp_docx_sections = []
#     while True:
#         if len(stack) < 2:
#             break
#         tmp_docx_section = stack.pop()
#         tmp_docx_sections.append(tmp_docx_section)
#         if tmp_docx_section.heading_level > stack[-1].heading_level:
#             stack[-1].sub_sections = tmp_docx_sections[::-1]
#             tmp_docx_sections = []
#
#     return stack[0]
#
#
# def print_docx_sections(docx_section: DocxSection):
#     print(f'{"-" * docx_section.heading_level}{docx_section.title}')
#     print(f'{"-" * docx_section.heading_level}{docx_section.text}')
#     for section in docx_section.sub_sections:
#         print_docx_sections(section)
#
#
# def filter_title(title: str) -> str:
#     # 过滤掉文档中标题的编号
#     return title.split(' ', 1)[-1]
#
#
# def wrap_itemized_resp(resp: List) -> List[str]:
#     res = []
#     for group in resp:
#         for item in group:
#             if item:
#                 res.append(item)
#     return res
#
#
# def generate_elementui_tree(docx_section: DocxSection):
#     grpc_client = GrpcClient()
#     node = {
#         '_id': generate_uuid(),
#         'label': filter_title(docx_section.title),
#         'children': []
#     }
#     if docx_section.text:
#         time.sleep(0.2)
#         resp = grpc_client.itemized(docx_section.text)
#         wrapped_resp = wrap_itemized_resp(json.loads(resp)['result'])
#         for item in wrapped_resp:
#             node['children'].append({
#                 '_id': generate_uuid(),
#                 'label': item,
#                 'children': []
#             })
#     # 递归添加子节点
#     for section in docx_section.sub_sections:
#         node['children'].append(generate_elementui_tree(section))
#
#     return node


if __name__ == '__main__':
    pass
