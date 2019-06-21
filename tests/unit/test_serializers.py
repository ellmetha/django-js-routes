import json

import pytest

from js_routes.serializers import URLPatternsSerializer
from js_routes.test import override_and_reload_settings


class TestURLPatternsSerializer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.serializer = URLPatternsSerializer()

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping', ])
    def test_can_serialize_specific_urls_that_do_not_have_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping'] == '/ping/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_args', ])
    def test_can_serialize_specific_urls_that_have_unnamed_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_args'] == '/ping/<>/foo/<>/bar/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_kwargs', ])
    def test_can_serialize_specific_urls_that_have_named_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_kwargs'] == '/ping/<pk1>/foo/<pk2>/bar/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_optional_character', ])
    def test_can_serialize_specific_urls_that_have_optional_characters(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_character'] == '/ping/<>/foo/bar/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_optional_group', ])
    def test_can_serialize_specific_urls_that_have_an_optional_group(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_group'] == '/ping/<>/foo/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_optional_kwarg', ])
    def test_can_serialize_specific_urls_that_have_an_optional_kwarg(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_kwarg'] == '/ping/<>/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['included_test_with_args', ])
    def test_can_serialize_specific_urls_that_have_been_included(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['included_test_with_args'] == '/included/<pk1>/test/<>/foo/<>/bar/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_re_path', ])
    def test_can_serialize_specific_urls_that_have_a_regex_path(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_re_path'] == '/ping/<year>/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_path', ])
    def test_can_serialize_specific_urls_that_have_a_path_expression(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_path'] == '/ping/<year>/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_paths', ])
    def test_can_serialize_specific_urls_that_have_multiple_path_expressions(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_paths'] == '/ping/<year>/<month>/'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping_with_path_without_converter', ])
    def test_can_serialize_specific_urls_that_have_a_path_without_converter(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_path_without_converter'] == '/ping/<slug>/'
