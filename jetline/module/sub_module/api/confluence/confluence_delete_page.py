# -*- coding: utf-8 -*-

from ...abc.sub_module import SubModule
from ....sub_module_parameter.api.confluence.confluence_delete_page_parameter import ConfluenceDeletePageParameter
from .....container.container import Container
from .....command.api.confluence.confluence_delete_page_command import ConfluenceDeletePageCommand


class ConfluenceDeletePage(SubModule):

    def __init__(self, param: ConfluenceDeletePageParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.confluence_component_key.get()
            )
        command = \
            ConfluenceDeletePageCommand(
                component,
                self._parameter.page_title.get(),
                self._parameter.space_key.get(),
                self._parameter.headers.get()
            )
        command .execute()

    def tear_down(self):
        super().tear_down()
