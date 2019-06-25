from django.contrib.staticfiles.finders import find
from django.template.loader import render_to_string


def test_static_resolver_is_up_to_date():
    expected_result = render_to_string('js_routes/_base/static_resolver.js')
    with open(find('js/routes/resolver.js')) as fd:
        assert fd.read() == expected_result, 'static resolver should be regenerated'
