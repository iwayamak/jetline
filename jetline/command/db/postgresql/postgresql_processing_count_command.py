# -*- coding: utf-8 -*-

import logging
from abc import ABC

from .abc.postgresql_command import PostgreSQLCommand
from ....container.component.postgresql_component import PostgreSQLComponent
from ....exception.command_error import CommandError

logger = logging.getLogger('jetline')


class PostgreSQLProcessingCountCommand(PostgreSQLCommand, ABC):

    def __init__(self,
                 component: PostgreSQLComponent,
                 sql_str: str,
                 assert_eq: int = None,
                 assert_ne: int = None,
                 assert_ge: int = None,
                 assert_le: int = None):
        self._assert_eq = assert_eq
        self._assert_ne = assert_ne
        self._assert_ge = assert_ge
        self._assert_le = assert_le
        super().__init__(component, sql_str)

    def set_up(self):
        super().set_up()

    def run(self):
        super().run()
        if self._cursor.rowcount != 1:
            raise CommandError(return_code='row_count:{0}'.format(self._cursor.rowcount), cmd=self._mask_password())

        count = None
        for row in self._cursor:
            count = row[0]
            if not isinstance(count, int):
                raise CommandError(return_code='count:{0}'.format(count), cmd=self._mask_password())

        logger.info('count: {0}'.format(count))
        if self._assert_eq is not None:
            logger.debug(
                'count:{0} == assert_eq:{1}'.format(count, self._assert_eq)
            )
            if not (count == self._assert_eq):
                raise CommandError(
                    return_code='count:{0} == assert_eq:{1}'.format(count, self._assert_eq),
                    cmd=self._mask_password()
                )
        elif self._assert_ne is not None:
            logger.debug(
                'count:{0} != assert_ne:{1}'.format(count, self._assert_ne)
            )
            if not (count != self._assert_ne):
                raise CommandError(
                    return_code='count:{0} != assert_ne:{1}'.format(count, self._assert_ne),
                    cmd=self._mask_password()
                )
        elif self._assert_ge is not None and self._assert_le is not None:
            if self._assert_ge <= self._assert_le:
                logger.debug(
                    'assert_ge:{1} <= count:{0} <= assert_le:{2}'.format(count, self._assert_ge, self._assert_le)
                )
                if not (self._assert_ge <= count <= self._assert_le):
                    raise CommandError(
                        return_code='assert_ge:{1} <= count:{0} <= assert_le:{2}'.format(count, self._assert_ge,
                                                                                        self._assert_le),
                        cmd=self._mask_password()
                    )
            else:
                logger.debug(
                    'count:{0} <= assert_le:{2} or assert_ge:{1} <= count:{0}'.format(count, self._assert_ge,
                                                                                      self._assert_le)
                )
                if not (count <= self._assert_le or self._assert_ge <= count):
                    raise CommandError(
                        return_code='count:{0} <= assert_le:{2} or assert_ge:{1} <= count:{0}'.format(count,
                                                                                                     self._assert_ge,
                                                                                                     self._assert_le),
                        cmd=self._mask_password())
        elif self._assert_ge is not None:
            logger.debug(
                'assert_ge:{1} <= count:{0}'.format(count, self._assert_ge)
            )
            if not (self._assert_ge <= count):
                raise CommandError(
                    return_code='assert_ge:{1} <= count:{0}'.format(count, self._assert_ge),
                    cmd=self._mask_password()
                )
        elif self._assert_le is not None:
            logger.debug(
                'count:{0} <= assert_le:{1}'.format(count, self._assert_le)
            )
            if not (count <= self._assert_le):
                raise CommandError(
                    return_code='count:{0} <= assert_le:{1}'.format(count, self._assert_le),
                    cmd=self._mask_password()
                )
        else:
            raise CommandError(
                return_code='Undefined assert_eq, assert_ne, assert_ge, assert_le.',
                cmd=self._mask_password()
            )

    def dry_run(self):
        super().dry_run()
        logger.info('count')
        if self._assert_eq is not None:
            logger.debug('count == assert_eq:{0}'.format(self._assert_eq))
        elif self._assert_ne is not None:
            logger.debug('count != assert_ne:{0}'.format(self._assert_ne))
        elif self._assert_ge is not None and self._assert_le is not None:
            if self._assert_ge <= self._assert_le:
                logger.debug(
                    'assert_ge:{0} <= count: <= assert_le:{1}'.format(self._assert_ge, self._assert_le)
                )
            else:
                logger.debug(
                    'count <= assert_le:{1} or assert_ge:{0} <= count'.format(self._assert_ge, self._assert_le)
                )
        elif self._assert_ge is not None:
            logger.debug('assert_ge:{0} <= count'.format(self._assert_ge))
        elif self._assert_le is not None:
            logger.debug('count <= assert_le:{0}'.format(self._assert_le))
        else:
            raise CommandError(
                return_code='Undefined assert_eq, assert_ne, assert_ge, assert_le.',
                cmd=self._mask_password())

    def tear_down(self):
        super().tear_down()
