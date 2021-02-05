# -*- coding: utf-8 -*-

from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue
from .....validator.validator import Validator


class PostgreSQLCopyFromParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._postgresql_component_key = None
        self._table_name = None
        self._column_list = None
        self._csv_file_name = None
        self._delimiter = None
        self._null_str = None
        self._header = None
        self._quote = None
        self._escape = None
        self._encoding = None
        self._gzip = None
        self._use_last_result = None
        self._remove_source_file = None
        super().__init__(params)

    @property
    def postgresql_component_key(self):
        return self._postgresql_component_key

    @postgresql_component_key.setter
    @Validator.component_key
    def postgresql_component_key(self, v):
        self._postgresql_component_key = MustValue(v)

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, v):
        self._table_name = MustValue(v)

    @property
    def column_list(self):
        return self._column_list

    @column_list.setter
    @Validator.list
    def column_list(self, v):
        self._column_list = OptionValue(v, default=None)

    @property
    def csv_file_name(self):
        return self._csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, v):
        self._csv_file_name = OptionValue(v)

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, v):
        self._delimiter = OptionValue(v, default=',')

    @property
    def null_str(self):
        return self._null_str

    @null_str.setter
    def null_str(self, v):
        self._null_str = OptionValue(v)

    @property
    def header(self):
        return self._header

    @header.setter
    @Validator.boolean
    def header(self, v):
        self._header = OptionValue(v, default=True)

    @property
    def quote(self):
        return self._quote

    @quote.setter
    def quote(self, v):
        self._quote = OptionValue(v, default='"')

    @property
    def escape(self):
        return self._escape

    @escape.setter
    def escape(self, v):
        self._escape = OptionValue(v, default='"')

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, v):
        self._encoding = OptionValue(v, default='utf8')

    @property
    def gzip(self):
        return self._gzip

    @gzip.setter
    @Validator.boolean
    def gzip(self, v):
        self._gzip = OptionValue(v, default=False)

    @property
    def use_last_result(self):
        return self._use_last_result

    @use_last_result.setter
    @Validator.boolean
    def use_last_result(self, v):
        self._use_last_result = OptionValue(v, default=False)

    @property
    def remove_source_file(self):
        return self._remove_source_file

    @remove_source_file.setter
    @Validator.boolean
    def remove_source_file(self, v):
        self._remove_source_file = OptionValue(v, default=False)
