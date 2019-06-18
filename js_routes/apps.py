"""
    JS Routes app config
    ====================

    This module defines the application configuration class, which is made available to the Django
    app registry.

"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JSRoutesAppConfig(AppConfig):
    """ Application configuration class of the Django JS Routes application. """

    label = 'js_routes'
    name = 'js_routes'
    verbose_name = _('Javascript Routes')
