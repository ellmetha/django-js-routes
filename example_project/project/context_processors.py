"""
    Project context processors
    ==========================

    This module defines project-level context processors. These context processors should not
    involve too much logic and operations and should only be related to project's configuration.

"""

from django.conf import settings


def webpack(request):
    """ Inserts a Webpack dev server URL into the context. """
    return (
        {'WEBPACK_DEV_SERVER_URL': settings.WEBPACK_DEV_SERVER_URL, }
        if settings.WEBPACK_DEV_SERVER_STARTED else {}
    )
