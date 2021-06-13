"""
    JS Routes serializers
    =====================

    This modules defines serializer classes responsible for extracting Django URLs that should be
    exposed to the client side to a specific format (eg. JSON). The resoluting exports are likely to
    be used in a Javascript module to provide reverse lookup functionality on the client side.

"""

import json
import re
from urllib.parse import urljoin

from django.urls import get_resolver
from django.urls.resolvers import (LocalePrefixPattern, RegexPattern, RoutePattern, URLPattern,
                                   URLResolver)

from .conf import settings
from .utils.text import replace


class URLPatternsSerializer:
    """ The main class responsible for the serialization of the URLs exposed on the client side.

    This class implements a mechanism allowing to traverse the tree of URLs of a specific URL
    resolver in order to return the URLs that should be exposed on the client side in a specific
    format such as JSON. The exported object provides a mapping between fully qualified (namespaced)
    URL names and the corresponding paths.

    This class uses the default URL resolver if no one is set at initialization time.

    """

    _url_arg_re = re.compile(r'(\(.*?\))')
    _url_kwarg_re = re.compile(r'(\(\?P\<(.*?)\>.*?\))')
    _url_optional_char_re = re.compile(r'(?:\w|/)(?:\?|\*)')
    _url_optional_group_re = re.compile(r'\(\?\:.*\)(?:\?|\*)')
    _url_path_re = re.compile(r'<(.*?)>')

    def __init__(self, resolver=None):
        self.resolver = resolver or get_resolver()

    def to_json(self):
        """ Serializes the URLs to be exported in a JSON array. """
        return json.dumps(dict(self._parse()))

    def _parse(self):
        return self._parse_resolver(self.resolver)

    def _parse_resolver(
        self, resolver, parent_namespace=None, parent_url_prefix=None, include_all=False
    ):
        namespace = ':'.join(filter(lambda n: n, [parent_namespace, resolver.namespace]))
        include_all = include_all or (namespace in settings.INCLUSION_LIST)

        urls = []
        for url_pattern in resolver.url_patterns:
            if isinstance(url_pattern, URLResolver):
                url_prefix = urljoin(parent_url_prefix or '/', self._prepare_url_part(url_pattern))
                urls = urls + self._parse_resolver(
                    url_pattern,
                    parent_namespace=namespace,
                    parent_url_prefix=url_prefix,
                    include_all=include_all
                )
            elif isinstance(url_pattern, URLPattern) and url_pattern.name:
                url_name = ':'.join(filter(lambda n: n, [namespace, url_pattern.name]))
                if url_name in settings.INCLUSION_LIST or include_all:
                    full_url = self._prepare_url_part(url_pattern)
                    urls.append((url_name, urljoin(parent_url_prefix or '/', full_url)))

        return urls

    def _prepare_url_part(self, url_pattern):
        url = ''

        if isinstance(url_pattern.pattern, RegexPattern):
            url = url_pattern.pattern._regex
        elif isinstance(url_pattern.pattern, RoutePattern):
            url = url_pattern.pattern._route
        elif isinstance(url_pattern.pattern, LocalePrefixPattern):
            url = str(url_pattern.pattern.regex)
        else:  # pragma: no cover
            raise ValueError(
                'url_pattern must be a valid URL pattern ; "{}" is not'.format(url_pattern)
            )

        final_url = replace(url, [('^', ''), ('$', '')])
        final_url = self._remove_optional_groups_from_url(final_url)
        final_url = self._remove_optional_characters_from_url(final_url)
        final_url = self._replace_arguments_in_url(final_url)

        return final_url

    def _remove_optional_groups_from_url(self, url):
        matches = self._url_optional_group_re.findall(url)
        return replace(url, [(el, '') for el in matches]) if matches else url

    def _remove_optional_characters_from_url(self, url):
        matches = self._url_optional_char_re.findall(url)
        return replace(url, [(el, '') for el in matches]) if matches else url

    def _replace_arguments_in_url(self, url):
        # Identifies and replaces named URL arguments inside the URL.
        kwarg_matches = self._url_kwarg_re.findall(url)
        url = (
            replace(url, [(el[0], '<{}>'.format(el[1])) for el in kwarg_matches])
            if kwarg_matches else url
        )

        # Identifies and replaces unnamed URL arguments inside the URL.
        args_matches = self._url_arg_re.findall(url)
        url = (
            replace(url, [(el, '<>') for el in args_matches]) if args_matches else url
        )

        # Identifies and replaces path expression (and associated converters) inside the URL.
        path_matches = self._url_path_re.findall(url)
        url = (
            replace(url, [(el, el.split(':')[-1]) for el in path_matches])
            if (path_matches and not (kwarg_matches or args_matches)) else url
        )

        return url


url_patterns_serializer = URLPatternsSerializer()
