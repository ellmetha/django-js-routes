import json
import unittest.mock

import pytest

from js_routes.serializers import URLPatternsSerializer


class TestURLPatternsSerializer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.serializer = URLPatternsSerializer()

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping', ])
    def test_can_serialize_specific_urls_that_do_not_have_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping'] == '/ping/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_args', ])
    def test_can_serialize_specific_urls_that_have_unnamed_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_args'] == '/ping/<>/foo/<>/bar/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_kwargs', ])
    def test_can_serialize_specific_urls_that_have_named_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_kwargs'] == '/ping/<pk1>/foo/<pk2>/bar/'

    @unittest.mock.patch(
        'js_routes.conf.settings.INCLUSION_LIST',
        ['ping_with_optional_character', ]
    )
    def test_can_serialize_specific_urls_that_have_optional_characters(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_character'] == '/ping/<>/foo/bar/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_optional_group', ])
    def test_can_serialize_specific_urls_that_have_an_optional_group(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_group'] == '/ping/<>/foo/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_optional_kwarg', ])
    def test_can_serialize_specific_urls_that_have_an_optional_kwarg(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_optional_kwarg'] == '/ping/<>/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['included_test_with_args', ])
    def test_can_serialize_specific_urls_that_have_been_included(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['included_test_with_args'] == '/included/<pk1>/test/<>/foo/<>/bar/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_re_path', ])
    def test_can_serialize_specific_urls_that_have_a_regex_path(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_re_path'] == '/ping/<year>/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_path', ])
    def test_can_serialize_specific_urls_that_have_a_path_expression(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_path'] == '/ping/<year>/'

    @unittest.mock.patch('js_routes.conf.settings.INCLUSION_LIST', ['ping_with_paths', ])
    def test_can_serialize_specific_urls_that_have_multiple_path_expressions(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_paths'] == '/ping/<year>/<month>/'

    @unittest.mock.patch(
        'js_routes.conf.settings.INCLUSION_LIST',
        ['ping_with_path_without_converter', ]
    )
    def test_can_serialize_specific_urls_that_have_a_path_without_converter(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict['ping_with_path_without_converter'] == '/ping/<slug>/'
