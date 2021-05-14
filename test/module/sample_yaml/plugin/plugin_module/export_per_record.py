# -*- coding: utf-8 -*-

import os
import logging
from jetline.container.container import Container
from jetline.util.file_util import FileUtil
from jetline.command.db.postgresql.abc.postgresql_command import PostgreSQLCommand

logger = logging.getLogger('jetline')


class ExportPerRecord(PostgreSQLCommand):

    def __init__(self, kwargs: dict):
        component = Container.component(kwargs['component_key'])
        sql_str = FileUtil.file_to_str(kwargs['sql_file_name'])
        self._output_dir = kwargs['output_dir']
        super().__init__(component, sql_str)

    def set_up(self):
        super().set_up()
        os.makedirs(self._output_dir, exist_ok=True)

    def body(self):
        super().body()

    def run(self):
        super().run()
        self._cursor = self._connection.cursor(name='server_cursor')
        self._cursor.execute(self._query)
        uniq_check_list = []
        for row in self._cursor:
            if row[0] in uniq_check_list:
                file_base_name, ext = os.path.splitext(row[0])
                file_name = \
                    os.path.join(
                        self._output_dir,
                        f'{file_base_name}_{uniq_check_list.count(row[0])}{ext}'
                    )
            else:
                file_name = os.path.join(self._output_dir, row[0])

            entity = row[1]
            FileUtil.str_to_file(file_name, entity)
            uniq_check_list.append(row[0])

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
