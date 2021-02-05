# -*- coding: utf-8 -*-

import logging
import subprocess
from abc import ABCMeta
from typing import Union
from ..abc.command import Command
from ...container.component.abc.component import Component

logger = logging.getLogger('jetline')


class SubprocessCommand(Command, metaclass=ABCMeta):

    def __init__(self, component: Union[Component, None],
                 cmd: list, check: bool = True, cwd: str = None, env: dict = None,
                 timeout: int = 43200):
        self._cmd = cmd
        self._check = check
        self._timeout = timeout
        self._return_code = None
        self._stdout = None
        self._cwd = cwd
        self._env = env
        super().__init__(component)

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        super().run()
        logger.info(f'command: {" ".join(self._cmd)}')
        if self._check:
            try:
                self._stdout = \
                    subprocess.check_output(
                        map(str, self._cmd),
                        stderr=subprocess.STDOUT,
                        cwd=self._cwd,
                        env=self._env,
                        timeout=self._timeout
                    )
            except subprocess.CalledProcessError as e:
                logger.error(
                    f'subprocess error. return code:{e.returncode}, output:{e.output.decode("utf-8")}'
                )
                raise e
            self._return_code = 0
        else:
            ps = \
                subprocess.Popen(
                    map(str, self._cmd),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=self._cwd,
                    env=self._env
                )
            (self._stdout, stderr) = ps.communicate(timeout=self._timeout)
            self._return_code = ps.returncode
        logger.info(f'subprocess return code: {self._return_code}')

    def dry_run(self):
        super().dry_run()
        logger.info(f'command: {" ".join(self._cmd)}')

    def tear_down(self):
        super().tear_down()
