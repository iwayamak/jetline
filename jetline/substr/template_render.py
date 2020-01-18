# -*- coding: utf-8 -*-

from jinja2 import Template
from ..substr.template_string.template_string import TemplateString
from ..share_parameter.share_parameter import ShareParameter


class TemplateRender(object):

    def __init__(self, src_str: str):
        self._src_str = src_str
        self._result = None

    def apply(self):
        result_str = self.evaluate()
        return result_str

    def evaluate(self):
        template = Template(self._src_str)
        data = {
            'batch_name': ShareParameter.batch_name,
            'exec_date': TemplateString.exec_date,
            'log_dir': ShareParameter.log_dir,
            'timestamp': TemplateString.timestamp
        }
        result = template.render(data)
        return result
