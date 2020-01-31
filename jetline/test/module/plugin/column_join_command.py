# -*- coding: utf-8 -*-

import csv
import logging
from jetline.command.abc.custom_command import CustomCommand

logger = logging.getLogger('jetline')


class ColumnJoinCommand(CustomCommand):

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        target_file_list = self._kwargs['target_files']
        result_file = self._kwargs['result_file']
        data_array = []
        super().run()
        for target_file in target_file_list:
            logger.info(f'loading "{target_file}"')
            with open(target_file, mode='r', newline='', encoding='utf-8') as file_obj:
                csv_reader = csv.reader(file_obj)
                read_data = [row for row in csv_reader]
                if len(data_array) < 1:
                    data_array = read_data
                else:
                    for i in range(len(read_data)):
                        data_array[i].extend(read_data[i])

        with open(self._kwargs['result_file'], mode='w', newline='', encoding='utf-8') as fo:
            logger.info(f'Exporting to {result_file}')
            csv_writer = csv.writer(fo)
            csv_writer.writerows(data_array)
        logger.info('Processing is complete.')

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
