# -*- coding: utf-8 -*-

from ...abc.sub_module import SubModule
from ....sub_module_parameter.db.postgresql.postgresql_copy_to_parameter import PostgreSQLCopyToParameter
from .....container.container import Container
from .....command.db.postgresql.postgresql_copy_to_command import PostgreSQLCopyToCommand
from .....util.file_util import FileUtil


class PostgreSQLCopyTo(SubModule):

    def __init__(self, param: PostgreSQLCopyToParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        command = \
            PostgreSQLCopyToCommand(
                component,
                FileUtil.file_to_str(
                    self._parameter.sql_file_name.get(),
                    self._parameter.input_value.get()
                ),
                self._parameter.csv_file_name.get(),
                self._parameter.delimiter.get(),
                self._parameter.null_str.get(),
                self._parameter.header.get(),
                self._parameter.quote.get(),
                self._parameter.escape.get(),
                self._parameter.force_quote_list.get(),
                self._parameter.encoding.get(),
                self._parameter.gzip.get(),
        )
        command.execute()
        self._result_local_file_list = [self._parameter.csv_file_name.get()]

    def tear_down(self):
        super().tear_down()
