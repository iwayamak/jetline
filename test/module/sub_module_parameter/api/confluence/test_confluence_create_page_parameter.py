# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.api.confluence.confluence_create_page_parameter import ConfluenceCreatePageParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestConfluenceCreatePageParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = 'CONFLUENCE_COMPONENT.ID=UT'
        self._page_title = os.path.splitext(os.path.basename(__file__))[0]
        self._space_key = 'SPC'
        self._ancestors_id = '2392085'
        self._headers = {'content-type': 'application/json'}
        self._json_file_name = \
            os.path.join(
                os.path.dirname(__file__),
                'test_data',
                'test_confluence_parameter.json'
            )
        self._description = f'created by {os.path.basename(__file__)}'
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = ConfluenceCreatePageParameter(
            {
                'confluence_component_key': self._component,
                'page_title': self._page_title,
                'space_key': self._space_key,
                'ancestors_id': self._ancestors_id,
                'headers': self._headers,
                'json_file_name': self._json_file_name,
                'description': self._description
            }
        )
        self.assertEqual(self._component, param.confluence_component_key.get())
        self.assertEqual(self._page_title, param.page_title.get())
        self.assertEqual(self._space_key, param.space_key.get())
        self.assertEqual(self._ancestors_id, param.ancestors_id.get())
        self.assertEqual(self._headers, param.headers.get())
        self.assertEqual(self._json_file_name, param.json_file_name.get())
        self.assertEqual(self._description, param.description.get())

    def test_must_parameter(self):
        param = ConfluenceCreatePageParameter(
            {
                'confluence_component_key': self._component,
                'page_title': self._page_title,
                'space_key': self._space_key,
                'ancestors_id': self._ancestors_id,
                'headers': self._headers,
                'json_file_name': self._json_file_name
            }
        )
        self.assertEqual(self._component, param.confluence_component_key.get())
        self.assertEqual(self._page_title, param.page_title.get())
        self.assertEqual(self._space_key, param.space_key.get())
        self.assertEqual(self._ancestors_id, param.ancestors_id.get())
        self.assertEqual(self._headers, param.headers.get())
        self.assertEqual(self._json_file_name, param.json_file_name.get())
        self.assertEqual('Please enter a description.', param.description.get())

    def test_component_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                    'ancestors_id': self._ancestors_id,
                    'headers': self._headers,
                    'json_file_name': self._json_file_name
                }
            )

    def test_page_title_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'confluence_component_key': self._component,
                    'space_key': self._space_key,
                    'ancestors_id': self._ancestors_id,
                    'headers': self._headers,
                    'json_file_name': self._json_file_name
                }
            )

    def test_space_key_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'ancestors_id': self._ancestors_id,
                    'headers': self._headers,
                    'json_file_name': self._json_file_name
                }
            )

    def test_ancestors_id_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                    'headers': self._headers,
                    'json_file_name': self._json_file_name
                }
            )

    def test_headers_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                    'ancestors_id': self._ancestors_id,
                    'json_file_name': self._json_file_name
                }
            )

    def test_json_file_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ConfluenceCreatePageParameter(
                {
                    'confluence_component_key': self._component,
                    'page_title': self._page_title,
                    'space_key': self._space_key,
                    'ancestors_id': self._ancestors_id,
                    'headers': self._headers
                }
            )
