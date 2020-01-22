# -*- coding: utf-8 -*-

from .abc.sub_module import SubModule
from ...container.container import Container
from ...command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from ..sub_module_parameter.postgresql_copy_from_parameter import PostgreSQLCopyFromParameter


class PostgreSQLCopyFrom(SubModule):

    def __init__(self, param: PostgreSQLCopyFromParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        command = \
            PostgreSQLCopyFromCommand(
                component,
                self._parameter.table_name.get(),
                self._parameter.csv_file_name.get(),
                self._parameter.delimiter.get(),
                self._parameter.null_str.get(),
                self._parameter.header.get(),
                self._parameter.quote.get(),
                self._parameter.escape.get(),
                self._parameter.gzip.get()
            )
        command.execute()

    def tear_down(self):
        super().tear_down()
