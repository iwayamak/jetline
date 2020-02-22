# -*- coding: utf-8 -*-

from .postgresql_processing_parameter import PostgreSQLProcessingParameter
from ...value.option_value import OptionValue
from .....validator.validator import Validator


class PostgreSQLProcessingCountParameter(PostgreSQLProcessingParameter):

    def __init__(self, params=None):
        self._assert_eq = None
        self._assert_ne = None
        self._assert_ge = None
        self._assert_le = None
        super().__init__(params)

    @property
    def assert_eq(self):
        return self._assert_eq

    @assert_eq.setter
    @Validator.digit
    def assert_eq(self, v):
        self._assert_eq = OptionValue(v)

    @property
    def assert_ne(self):
        return self._assert_ne

    @assert_ne.setter
    @Validator.digit
    def assert_ne(self, v):
        self._assert_ne = OptionValue(v)

    @property
    def assert_ge(self):
        return self._assert_ge

    @assert_ge.setter
    @Validator.digit
    def assert_ge(self, v):
        self._assert_ge = OptionValue(v)

    @property
    def assert_le(self):
        return self._assert_le

    @assert_le.setter
    @Validator.digit
    def assert_le(self, v):
        self._assert_le = OptionValue(v)
