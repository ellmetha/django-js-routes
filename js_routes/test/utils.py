"""
    JS Routes test utilities
    ========================

    This modules defines utilities that can be used when testing the JS routes application.

"""

import imp

from django.test.utils import override_settings

from ..conf import settings as js_routes_settings


class override_and_reload_settings(override_settings):
    """ Context manager allowing to override settings and reload the JS routes settings module. """

    def __enter__(self):
        super().__enter__()
        imp.reload(js_routes_settings)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        imp.reload(js_routes_settings)
