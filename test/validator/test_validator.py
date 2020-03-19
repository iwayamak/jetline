# -*- coding: utf-8 -*-

import os
import datetime
from jetline.validator.validator import Validator
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from ..abc.base_test_case import BaseTestCase


class TestValidator(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestValidator, self).__init__(*args, **kwargs)

    @Validator.path
    def set_path(self, s):
        pass

    def test_path(self):
        file = \
            os.path.join(
                os.path.dirname(__file__), 'test_validator.tsv'
            )
        file2 = \
            os.path.join(
                os.path.dirname(__file__), 'test_validator2.tsv'
            )
        self.set_path(file)
        self.set_path(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_path(file2)

    @Validator.component_key
    def set_component_key(self, key):
        pass

    def test_component_key(self):
        self.set_component_key('POSTGRESQL_COMPONENT.ID=UT')
        self.set_component_key(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_component_key('invalid')

    @Validator.digit
    def set_digit(self, key):
        pass

    def test_digit(self):
        self.set_digit(123)
        self.set_digit('123')
        self.set_digit(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_digit('1.1')
        with self.assertRaises(SubModuleParameterError):
            self.set_digit('12a')
        with self.assertRaises(SubModuleParameterError):
            self.set_digit(datetime.datetime.now())

    @Validator.boolean
    def set_boolean(self, key):
        pass

    def test_boolean(self):
        self.set_boolean(True)
        self.set_boolean(False)
        self.set_boolean('true')
        self.set_boolean('FALSE')
        self.set_boolean('on')
        self.set_boolean('oFF')
        self.set_boolean('1')
        self.set_boolean(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean('abc')
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean('OK')
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(0)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(-1)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(datetime.datetime.now())

    @Validator.regexp('^(append|replace|truncate|update)$')
    def set_regexp(self, key):
        pass

    def test_regexp(self):
        self.set_regexp('append')
        self.set_regexp('replace')
        self.set_regexp('truncate')
        self.set_regexp('update')
        self.set_regexp(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp('app')
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp('appendappend')
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp('ab_replace_c')
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp('delete')
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(111)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(True)

    @Validator.range(-2, 2)
    def set_range(self, key):
        pass

    def test_range(self):
        self.set_range(-2)
        self.set_range(0)
        self.set_range(+1)
        self.set_range(2)
        self.set_range(-1.1)
        self.set_range(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_range('app')
        with self.assertRaises(SubModuleParameterError):
            self.set_range('1')
        with self.assertRaises(SubModuleParameterError):
            self.set_range(-2.1)
        with self.assertRaises(SubModuleParameterError):
            self.set_range(2.1)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(False)

    @Validator.list
    def set_list(self, key):
        pass

    def test_list(self):
        self.set_list(['item', 'item2'])
        self.set_list([])
        self.set_list(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_list(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_list('list')
        with self.assertRaises(SubModuleParameterError):
            self.set_list(datetime.datetime.now())

    @Validator.dict
    def set_dict(self, key):
        pass

    def test_dict(self):
        self.set_dict({'key1': 'item', 'key2': 'item2'})
        self.set_dict({})
        self.set_dict(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_dict('dict')
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(datetime.datetime.now())
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(['item', 'item2'])
        with self.assertRaises(SubModuleParameterError):
            self.set_dict([])
