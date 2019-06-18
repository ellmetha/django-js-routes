"""
    JS Routes settings
    ==================

    This file defines settings that can be overriden in the Django project's settings module.

"""

from django.conf import settings


# The "INCLUSION_LIST" setting allows to define which URLs should be serialized and made available
# to the client side through the generated/exported Javascript helper. The list should contain URL
# name or namespaces. If a namespace is included in this list, all the underlying URLs will be
# made available to the client side.
INCLUSION_LIST = getattr(settings, 'JS_ROUTES_INCLUSION_LIST', [])
