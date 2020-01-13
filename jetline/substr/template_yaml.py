# -*- coding: utf-8 -*-

from .template import Template


class TemplateYaml(Template):

    def __init__(self, src_str: str):
        super().__init__(src_str, query_mode=False)
