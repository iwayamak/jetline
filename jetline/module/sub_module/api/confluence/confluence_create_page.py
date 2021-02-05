# -*- coding: utf-8 -*-

from ...abc.sub_module import SubModule
from ....sub_module_parameter.api.confluence.confluence_create_page_parameter import ConfluenceCreatePageParameter
from .....container.container import Container
from .....command.api.confluence.confluence_create_page_command import ConfluenceCreatePageCommand
from .....util.file_util import FileUtil


class ConfluenceCreatePage(SubModule):

    def __init__(self, param: ConfluenceCreatePageParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.confluence_component_key.get()
            )
        command = \
            ConfluenceCreatePageCommand(
                component,
                self._parameter.page_title.get(),
                self._parameter.space_key.get(),
                self._parameter.ancestors_id.get(),
                self._parameter.headers.get(),
                FileUtil.json_to_html_table(
                    self._parameter.json_file_name.get()
                ),
                self._parameter.description.get()
            )
        command .execute()

    def tear_down(self):
        super().tear_down()
