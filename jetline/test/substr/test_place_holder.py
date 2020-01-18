# -*- coding: utf-8 -*-

import os
from ..abc.base_test_case import BaseTestCase
from ...substr.place_holder import PlaceHolder


class TestPlaceHolder(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_exec(self):
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_place_holder.txt'
            )
        correct_result = 'hello good-bye'
        template = PlaceHolder(
            filename,
            {
                'elem_1': 'hello',
                'elem_2': 'good-bye',
                'elem_3': 'see you'
            }
        )
        result = template.apply()
        self.assertEqual(correct_result, result)
