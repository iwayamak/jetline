# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader
from ..substr.template_string.template_string import TemplateString
from ..share_parameter.share_parameter import ShareParameter
from ..util.path_util import PathUtil


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
        self._input_value.update(
            {
                'batch_name': ShareParameter.batch_name,
                'exec_date': TemplateString.exec_date,
                'log_dir': ShareParameter.log_dir,
                'timestamp': TemplateString.timestamp,
                'jetline_root': PathUtil.jetline_root_path()
            }
        )
        env = Environment(
            loader=FileSystemLoader(template_dir, encoding='utf-8')
        )
        template = env.get_template(
            os.path.basename(self._filename)
        )
        result = template.render(self._input_value)
        return result
