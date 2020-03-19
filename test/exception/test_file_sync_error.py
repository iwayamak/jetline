# -*- coding: utf-8 -*-

from jetline.exception.file_sync_error import FileSyncError
from ..abc.base_test_case import BaseTestCase


class TestFileSyncError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(FileSyncError):
            raise FileSyncError('file sync error')
