"""
    Development Django settings
    ===========================

    This file imports the ``base`` settings and can add or modify previously defined settings to
    alter the configuration of the application for development purposes.

    For more information on this file, see https://docs.djangoproject.com/en/dev/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/dev/ref/settings/

"""

import socket

from .base import *  # noqa


# APP CONFIGURATION
# ------------------------------------------------------------------------------

INSTALLED_APPS += (  # noqa: F405
    'debug_toolbar',
)


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE += (  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# DEBUG CONFIGURATION
# ------------------------------------------------------------------------------

DEBUG = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ]
INTERNAL_IPS = ['127.0.0.1', ]


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

TEMPLATES[0]['OPTIONS']['context_processors'] += (  # noqa: F405
    'project.context_processors.webpack', )
TEMPLATES[0]['OPTIONS']['loaders'] = (  # noqa: F405
    # Disables cached loader
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------

STATICFILES_DIRS = (
    str(PROJECT_PATH / 'main' / 'static' / 'build_dev'),  # noqa: F405
    str(PROJECT_PATH / 'main' / 'static' / 'build'),  # noqa: F405
    str(PROJECT_PATH / 'main' / 'static'),  # noqa: F405
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# WEBPACK-DEV-SERVER CONFIGURATION
# ------------------------------------------------------------------------------

WEBPACK_DEV_SERVER_PORT = get_envsetting('WEBPACK_DEV_SERVER_PORT', 8080)  # noqa: F405
WEBPACK_DEV_SERVER_URL = 'http://localhost:{}'.format(WEBPACK_DEV_SERVER_PORT)

# Dynamically set a boolean indicating if the webpack dev server is started.
webpack_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    webpack_sock.bind(('localhost', WEBPACK_DEV_SERVER_PORT))
    WEBPACK_DEV_SERVER_STARTED = False
except socket.error as e:
    WEBPACK_DEV_SERVER_STARTED = (e.errno == 48 or e.errno == 98 or e.errno == 99)
webpack_sock.close()
