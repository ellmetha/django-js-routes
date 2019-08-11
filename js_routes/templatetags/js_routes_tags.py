"""
    JS Routes template tags
    =======================

    This module defines the template tags that can be used to include serialized sets of URLs in
    Django templates.

"""

from django import template

from ..serializers import url_patterns_serializer


register = template.Library()


@register.inclusion_tag('js_routes/routes.html', takes_context=False)
def js_routes(routes_only=False):
    """ Includes the serialized version of the exposed URLs in the template. """
    return {
        'routes': url_patterns_serializer.to_json(),
        'routes_only': routes_only,
    }
