"""
    JS Routes resolver helpers
    ==========================

    This modules defines helper functions allowing to build client resolver helpers.

"""

import os.path as op

import django
from django.conf import settings
from django.template.loader import render_to_string


settings.configure(
    DEBUG=True,
    INSTALLED_APPS=['js_routes', ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (),
            'OPTIONS': {
                'loaders': ['django.template.loaders.app_directories.Loader', ],
            },
        },
    ],
    ROOT_URLCONF=None,
)
django.setup()


def _build_static_resolver():
    path = op.join(op.dirname(op.abspath(__file__)), '../static/js/routes/resolver.js')
    with open(path, mode='w') as fd:
        fd.write(render_to_string('js_routes/_base/static_resolver.js'))


if __name__ == '__main__':
    _build_static_resolver()
