# -*- coding: utf-8 -*-

import json
from json2html import json2html
from typing import Union
from ..substr.place_holder import PlaceHolder


class FileUtil(object):

    @classmethod
    def file_to_str(cls, filename: str, input_value: Union[dict, None] = None):
        if input_value is None:
            input_value = {}
        place_holder = PlaceHolder(filename, input_value)
        s = place_holder.apply()
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
    def tsv_str_to_html_table(cls, tsv_contents: str, column_str: str):
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

    @classmethod
    def json_to_html_table(cls, filename: str):
        with open(filename) as file:
            data_dict = json.load(file)
            html_table = json2html.convert(json=data_dict, escape=False)
        return html_table

