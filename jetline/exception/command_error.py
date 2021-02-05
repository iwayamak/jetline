# -*- coding: utf-8 -*-


class CommandError(Exception):

    def __init__(self, return_code=None, cmd=None):
        info = 'Command \'{cmd}\' returned non-zero exit status {return_code}'
        self._info = info.format(cmd=cmd, return_code=return_code)

    def __str__(self):
        return repr(self._info)
