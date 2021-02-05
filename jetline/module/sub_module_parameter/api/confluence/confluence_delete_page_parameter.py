# -*- coding: utf-8 -*-

from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from .....validator.validator import Validator


class ConfluenceDeletePageParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._confluence_component_key = None
        self._page_title = None
        self._space_key = None
        self._headers = None
        super().__init__(params)

    @property
    def confluence_component_key(self):
        return self._confluence_component_key

    @confluence_component_key.setter
    @Validator.component_key
    def confluence_component_key(self, v):
        self._confluence_component_key = MustValue(v)

    @property
    def page_title(self):
        return self._page_title

    @page_title.setter
    def page_title(self, v):
        self._page_title = MustValue(v)

    @property
    def space_key(self):
        return self._space_key

    @space_key.setter
    def space_key(self, v):
        self._space_key = MustValue(v)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, v):
        self._headers = MustValue(v)
