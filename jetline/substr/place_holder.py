# -*- coding: utf-8 -*-

import logging
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger('jetline')


class PlaceHolder(object):

    def __init__(self, filename, input_value):
        self._filename = filename
        self._input_value = input_value

    def apply(self):
        logger.debug('replace target: ' + self._filename)
        result_str = self._evaluate()
        return result_str

    def _evaluate(self):
        env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
        tpl = env.get_template(self._filename)

        result = tpl.render(self._input_value)
        return result
