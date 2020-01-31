# -*- coding: utf-8 -*-

from .abc.sub_module import SubModule
from ...container.container import Container
from ...share_parameter.share_parameter import ShareParameter
from ...command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from ..sub_module_parameter.postgresql_copy_from_parameter import PostgreSQLCopyFromParameter


class PostgreSQLCopyFrom(SubModule):

    def __init__(self, param: PostgreSQLCopyFromParameter):
        super().__init__(param)

    def run(self):
        csv_file_name_list = [self._parameter.csv_file_name.get()]
        if self._parameter.use_last_result.get():
            csv_file_name_list = \
                ShareParameter.sub_module_result.get_last_log_local_data_file_list()
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        command = \
            PostgreSQLCopyFromCommand(
                component,
                self._parameter.table_name.get(),
                self._parameter.column_list.get(),
                csv_file_name_list,
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
