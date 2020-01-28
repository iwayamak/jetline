# -*- coding: utf-8 -*-

from ..substr.place_holder import PlaceHolder
from ..substr.template_render import TemplateRender


class FileUtil(object):

    @classmethod
    def file_to_str(cls, filename: str, input_value: dict = None):
        if input_value is not None:
            place_holder = PlaceHolder(filename, input_value)
            s = place_holder.apply()
        else:
            with open(filename, encoding='utf8') as file:
                s = TemplateRender(file.read()).apply()
        return s

    @classmethod
    def str_to_file(cls, filename: str, text: str):
        with open(filename, mode='w', encoding='utf8') as file:
            s = file.write(text)
        return s

    @classmethod
    def str_to_file_append(cls, filename: str, text: str):
        with open(filename, mode='a', encoding='utf8') as file:
            s = file.write(text)
        return s

    @classmethod
    def tsv_str_to_html_table(self, tsv_contents:str, column_str:str):
        tsv_contents = column_str + tsv_contents
        tsv_lines = tsv_contents.split('\n')
        html_table = '<table>'
        for tsv_line in tsv_lines:
            html_table += '<tr>'
            tab_list = tsv_line.split('\t')
            for tab in tab_list:
                html_table += f'<td>{tab}</td>'
            html_table += '</tr>'
        html_table += '</table>'
        return html_table
