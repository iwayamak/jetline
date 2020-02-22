# -*- coding: utf-8 -*-

from ...abc.sub_module import SubModule
from ....sub_module_parameter.db.postgresql.postgresql_processing_parameter import PostgreSQLProcessingParameter
from .....container.container import Container
from .....command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from .....util.file_util import FileUtil


class PostgreSQLProcessing(SubModule):

    def __init__(self, param: PostgreSQLProcessingParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        command = \
            PostgreSQLProcessingCommand(
                component,
                FileUtil.file_to_str(
                    self._parameter.sql_file_name.get(),
                    self._parameter.input_value.get()
                )
            )
        command .execute()

    def tear_down(self):
        super().tear_down()
