# -*- coding: utf-8 *-


class ConfluenceError(Exception):

    def __init__(self, status_code: int, error_message: str):
        info = 'status code: {status_code}, error message : {error_message}'
        self._info = \
            info.format(
                status_code=str(status_code), error_message=error_message
            )

    def __str__(self):
        return repr(self._info)
