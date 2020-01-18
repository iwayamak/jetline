# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader


class PlaceHolder(object):

    def __init__(self, filename: str, input_value: dict):
        self._filename = filename
        self._input_value = input_value

    def apply(self):
        result_str = self._evaluate()
        return result_str

    def _evaluate(self):
        template_dir = os.path.abspath(
            os.path.dirname(
                self._filename
            )
        )
        env = Environment(
            loader=FileSystemLoader(template_dir, encoding='utf-8')
        )
        template = env.get_template(
            os.path.basename(self._filename)
        )
        result = template.render(self._input_value)
        return result
