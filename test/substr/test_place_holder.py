# -*- coding: utf-8 -*-

import os
from ..abc.base_test_case import BaseTestCase
from jetline.substr.place_holder import PlaceHolder
from jetline.share_parameter.share_parameter import ShareParameter


class TestPlaceHolder(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_exec(self):
        ShareParameter.exec_date = '20200401'
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_place_holder.txt'
            )
        correct_result = '20200401 hello good-bye'
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
