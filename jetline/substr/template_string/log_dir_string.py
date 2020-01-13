# -*- coding: utf-8 -*-

from .template_string import TemplateString
from ...share_parameter.share_parameter import ShareParameter


class LogDirString(TemplateString):

    SUB_STR = 'log_dir'

    def __init__(self):
        super().__init__()

    def evaluate(self):
        self._result = ShareParameter.log_dir
        super().evaluate()
