# -*- coding: utf-8 -*-

import glob
from ...abc.sub_module import SubModule
from ....sub_module_parameter.db.postgresql.postgresql_copy_from_parameter import PostgreSQLCopyFromParameter
from .....command.command_queue import CommandQueue
from .....command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from .....command.local.remove_command import RemoveCommand
from .....container.container import Container
from .....share_parameter.share_parameter import ShareParameter


class PostgreSQLCopyFrom(SubModule):

    def __init__(self, param: PostgreSQLCopyFromParameter):
        super().__init__(param)

    def run(self):
        if self._parameter.csv_file_name.get():
            csv_file_name_list = glob.glob(self._parameter.csv_file_name.get())
        if self._parameter.use_last_result.get():
            csv_file_name_list = \
                ShareParameter.sub_module_result.get_last_log_local_data_file_list()
        component = \
            Container.component(
                self._parameter.postgresql_component_key.get()
            )
        queue = CommandQueue()
        queue.add_command(
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
                self._parameter.encoding.get(),
                self._parameter.gzip.get()
            )
        )
        if self._parameter.remove_source_file.get():
            for csv_file_name in csv_file_name_list:
                queue.add_command(
                    RemoveCommand(csv_file_name)
                )
        queue.execute()

    def tear_down(self):
        super().tear_down()
