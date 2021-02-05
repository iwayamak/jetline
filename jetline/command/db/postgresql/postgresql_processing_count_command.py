# -*- coding: utf-8 -*-

import logging

from .abc.postgresql_command import PostgreSQLCommand
from ....container.component.postgresql_component import PostgreSQLComponent
from ....exception.command_error import CommandError

logger = logging.getLogger('jetline')


class PostgreSQLProcessingCountCommand(PostgreSQLCommand):

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
        self._cursor.execute(self._query)
        self._connection.commit()
        if self._cursor.rowcount != 1:
            raise CommandError(
                return_code=f'row_count: {self._cursor.rowcount}',
                cmd=self._mask_password()
            )

        count = None
        for row in self._cursor:
            count = row[0]
            if not isinstance(count, int):
                raise CommandError(
                    return_code=f'count: {count}',
                    cmd=self._mask_password()
                )

        logger.info(f'count: {count}')
        if self._assert_eq is not None:
            logger.debug(
                f'count: {count} == assert_eq: {self._assert_eq}'
            )
            if not (count == self._assert_eq):
                raise CommandError(
                    return_code=f'count: {count} == assert_eq: {self._assert_eq}',
                    cmd=self._mask_password()
                )
        elif self._assert_ne is not None:
            logger.debug(
                f'count: {count} != assert_ne: {self._assert_ne}'
            )
            if not (count != self._assert_ne):
                raise CommandError(
                    return_code=f'count: {count} != assert_ne: {self._assert_ne}',
                    cmd=self._mask_password()
                )
        elif self._assert_ge is not None and self._assert_le is not None:
            if self._assert_ge <= self._assert_le:
                logger.debug(
                    f'assert_ge: {count} <= count: {self._assert_ge} <= assert_le: {self._assert_le}'
                )
                if not (self._assert_ge <= count <= self._assert_le):
                    raise CommandError(
                        return_code=f'assert_ge: {count} <= count: {self._assert_ge} <= assert_le: {self._assert_le}',
                        cmd=self._mask_password()
                    )
            else:
                logger.debug(
                    f'count: {count} <= assert_le: {self._assert_ge} or assert_ge: {self._assert_le} <= count: {count}'
                )
                if not (count <= self._assert_le or self._assert_ge <= count):
                    raise CommandError(
                        return_code=f'count: {count} <= assert_le: {self._assert_ge} or assert_ge: {self._assert_le} <= count:{count}',
                        cmd=self._mask_password())
        elif self._assert_ge is not None:
            logger.debug(
                f'assert_ge: {count} <= count: {self._assert_ge}'
            )
            if not (self._assert_ge <= count):
                raise CommandError(
                    return_code=f'assert_ge: {count} <= count: {self._assert_ge}',
                    cmd=self._mask_password()
                )
        elif self._assert_le is not None:
            logger.debug(
                f'count: {count} <= assert_le: {self._assert_le}'
            )
            if not (count <= self._assert_le):
                raise CommandError(
                    return_code=f'count: {count} <= assert_le: {self._assert_le}',
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
            logger.debug(f'count == assert_eq: {self._assert_eq}')
        elif self._assert_ne is not None:
            logger.debug(f'count != assert_ne: {self._assert_ne}')
        elif self._assert_ge is not None and self._assert_le is not None:
            if self._assert_ge <= self._assert_le:
                logger.debug(
                    f'assert_ge: {self._assert_ge} <= count: <= assert_le: {self._assert_le}'
                )
            else:
                logger.debug(
                    f'count <= assert_le: {self._assert_ge} or assert_ge: {self._assert_le} <= count'
                )
        elif self._assert_ge is not None:
            logger.debug(f'assert_ge: {self._assert_ge} <= count')
        elif self._assert_le is not None:
            logger.debug(f'count <= assert_le: {self._assert_le}')
        else:
            raise CommandError(
                return_code='Undefined assert_eq, assert_ne, assert_ge, assert_le.',
                cmd=self._mask_password())

    def tear_down(self):
        super().tear_down()
