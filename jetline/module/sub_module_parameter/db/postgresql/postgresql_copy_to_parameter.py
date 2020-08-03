# -*- coding: utf-8 -*-

from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue
from .....validator.validator import Validator


class PostgreSQLCopyToParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._postgresql_component_key = None
        self._sql_file_name = None
        self._csv_file_name = None
        self._delimiter = None
        self._null_str = None
        self._header = None
        self._quote = None
        self._escape = None
        self._force_quote_list = None
        self._encoding = None
        self._gzip = None
        self._input_value = None
        super().__init__(params)

    @property
    def postgresql_component_key(self):
        return self._postgresql_component_key

    @postgresql_component_key.setter
    @Validator.component_key
    def postgresql_component_key(self, v):
        self._postgresql_component_key = MustValue(v)

    @property
    def sql_file_name(self):
        return self._sql_file_name

    @sql_file_name.setter
    @Validator.path
    def sql_file_name(self, v):
        self._sql_file_name = MustValue(v)

    @property
    def csv_file_name(self):
        return self._csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, v):
        self._csv_file_name = MustValue(v)

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
    def force_quote_list(self):
        return self._force_quote_list

    @force_quote_list.setter
    @Validator.list
    def force_quote_list(self, v):
        self._force_quote_list = OptionValue(v)

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, v):
        self._encoding = OptionValue(v, default='utf-8')

    @property
    def gzip(self):
        return self._gzip

    @gzip.setter
    @Validator.boolean
    def gzip(self, v):
        self._gzip = OptionValue(v, default=False)

    @property
    def input_value(self):
        return self._input_value

    @input_value.setter
    @Validator.dict
    def input_value(self, v):
        self._input_value = OptionValue(v)
