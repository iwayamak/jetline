# -*- coding: utf-8 -*-

import logging
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class ScpCommand(Command):

    def __init__(self, component: Component):
        self.ssh = None
        self.scp = None
        super().__init__(component)

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(
            username=self.component.user,
            password=self.component.password,
            hostname=self.component.host,
            port=self.component.port
        )
        self.scp = SCPClient(self.ssh.get_transport(), sanitize=lambda x: x)
        super().run()

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
        self.scp.close()
        self.ssh.close()
