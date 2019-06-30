import tempfile
from io import StringIO

import pytest
from django.core.management import call_command
from django.template.loader import render_to_string

from js_routes.serializers import url_patterns_serializer


class TestDumpRoutesResolverCommand:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        yield
        self.stdout.close()
        self.stderr.close()

    def test_exports_the_routes_and_resolver_module_into_a_single_file(self):
        call_command('dump_routes_resolver', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read() == render_to_string(
            'js_routes/_dump/default.js',
            {'routes': url_patterns_serializer.to_json()}
        )

    def test_can_export_the_routes_and_resolver_module_into_a_single_file_in_the_default_format(self):  # noqa
        call_command('dump_routes_resolver', format='default', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read() == render_to_string(
            'js_routes/_dump/default.js',
            {'routes': url_patterns_serializer.to_json()}
        )

    def test_can_export_the_routes_and_resolver_module_into_a_single_file_in_an_es6_format(self):
        call_command('dump_routes_resolver', format='es6', stdout=self.stdout)
        self.stdout.seek(0)
        assert self.stdout.read() == render_to_string(
            'js_routes/_dump/es6.js',
            {'routes': url_patterns_serializer.to_json()}
        )

    def test_can_export_the_routes_and_resolver_module_into_a_specific_file(self):
        export_filename = tempfile.mktemp()
        call_command('dump_routes_resolver', output=export_filename, stdout=self.stdout)
        self.stdout.seek(0)
        with open(export_filename) as fd:
            assert fd.read() == render_to_string(
                'js_routes/_dump/default.js',
                {'routes': url_patterns_serializer.to_json()}
            )
