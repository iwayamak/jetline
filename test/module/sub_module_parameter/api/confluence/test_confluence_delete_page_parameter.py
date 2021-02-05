# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.api.confluence.confluence_delete_page_parameter import ConfluenceDeletePageParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestConfluenceDeletePageParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = 'CONFLUENCE_COMPONENT.ID=UT'
        self._page_title = os.path.splitext(os.path.basename(__file__))[0]
        self._space_key = 'SPC'
        self._headers = {'content-type': 'application/json'}
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = ConfluenceDeletePageParameter(
            {
                'confluence_component_key': self._component,
                'page_title': self._page_title,
                'space_key': self._space_key,
                'headers': self._headers,
            }
        )
        self.assertEqual(self._component, param.confluence_component_key.get())
        self.assertEqual(self._page_title, param.page_title.get())
        self.assertEqual(self._space_key, param.space_key.get())
        self.assertEqual(self._headers, param.headers.get())

    def test_component_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceDeletePageParameter(
                {
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                    'headers': self._headers,
                }
            )

    def test_page_title_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceDeletePageParameter(
                {
                    'confluence_component_key': self._component,
                    'space_key': self._space_key,
                    'headers': self._headers,
                }
            )

    def test_space_key_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceDeletePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'headers': self._headers,
                }
            )

    def test_headers_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceDeletePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                }
            )
