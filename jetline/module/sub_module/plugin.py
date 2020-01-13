# -*- coding: utf-8 -*-

import sys
import logging
import importlib
from .abc.sub_module import SubModule
from ...command.command_queue import CommandQueue
from ..sub_module_parameter.plugin_parameter import PluginParameter

logger = logging.getLogger('jetline')


class Plugin(SubModule):

    def __init__(self, param: PluginParameter):
        super().__init__(param)

    def run(self):
        plugin_path = self._parameter.plugin_path.get()
        logger.info('plugin_path: {0}'.format(plugin_path))
        sys.path.append(plugin_path)
        package = self._parameter.package.get()
        class_name = self._parameter.class_name.get()
        kwargs = self._parameter.kwargs.get()
        m = importlib.import_module(package)
        sub_module = getattr(m, class_name)(kwargs)

        queue = CommandQueue()
        queue.add_command(sub_module)
        queue.execute()

    def tear_down(self):
        super().tear_down()
