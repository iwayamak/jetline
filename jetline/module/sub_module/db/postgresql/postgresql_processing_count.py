# -*- coding: utf-8 -*-

from ...abc.sub_module import SubModule
from ....sub_module_parameter.db.postgresql.postgresql_processing_count_parameter import PostgreSQLProcessingCountParameter
from .....container.container import Container
from .....command.db.postgresql.postgresql_processing_count_command import PostgreSQLProcessingCountCommand
from .....util.file_util import FileUtil


class PostgreSQLProcessingCount(SubModule):

    def __init__(self, param: PostgreSQLProcessingCountParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        command = \
            PostgreSQLProcessingCountCommand(
                component,
                FileUtil.file_to_str(
                    self._parameter.sql_file_name.get(),
                    self._parameter.input_value.get()
                ),
                self._parameter.assert_eq.get(),
                self._parameter.assert_ne.get(),
                self._parameter.assert_ge.get(),
                self._parameter.assert_le.get()
            )
        command.execute()

    def tear_down(self):
        super().tear_down()
