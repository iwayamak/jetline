# -*- coding: utf-8 -*-

from .template_string import TemplateString
from ...share_parameter.share_parameter import ShareParameter


class BatchNameString(TemplateString):

    SUB_STR = 'batch_name'

    def __init__(self):
        super().__init__()

    def evaluate(self):
        self._result = ShareParameter.batch_name
        super().evaluate()
