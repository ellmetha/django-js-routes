from django.template import Context
from django.template.base import Template
from django.template.defaultfilters import safe

from js_routes.serializers import url_patterns_serializer
from js_routes.test import override_and_reload_settings


class TestJsRoutesTag:
    loadstatement = '{% load js_routes_tags %}'

    @override_and_reload_settings(JS_ROUTES_INCLUSION_LIST=['ping', ])
    def test_render_serialized_routes_inside_a_script_tag(self, rf):
        def get_rendered():
            t = Template(self.loadstatement + '{% js_routes %}')
            c = Context({})
            rendered = t.render(c)
            return rendered

        assert get_rendered().strip() == '<script>window.routes = {};</script>'.format(
            safe(url_patterns_serializer.to_json())
        )
