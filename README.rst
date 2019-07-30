django-js-routes
################

**Django-js-routes** is a Django application allowing to expose and perform reverse lookups of
Django named URL patterns on the client side.

.. contents:: Table of Contents
    :local:

Main requirements
=================

Python 3.4+, Django 2.0+.

Installation
============

To install Django-js-routes, please use the pip_ command as follows:

.. code-block:: shell

    $ pip install --pre django-js-routes

Once the package is installed, you'll have to add the application to ``INSTALLED_APPS`` in your
project's settings module:

.. code-block:: python

    INSTALLED_APPS = (
        # all other apps...
        'js_routes',
    )

You can then define which URL patterns or URL namespaces you want to expose to the client side by
setting the ``JS_ROUTES_INCLUSION_LIST`` setting. This setting allows to define which URLs should be
serialized and made available to the client side through the generated and / or exported Javascript
helper. This list should contain only URL pattern names or namespaces. Here is an example:

.. code-block:: python

    JS_ROUTES_INCLUSION_LIST = [
        'home',
        'catalog:product_list',
        'catalog:product_detail',
    ]

Note that if a namespace is included in this list, all the underlying URLs will be made available to
the client side through the generated Javascript helper. Django-js-routes is safe by design in the
sense that *only* the URLs that you configure in this inclusion list will be publicly exposed on the
client side.

Once the list of URLs to expose is configured, you can add the `{% js_routes %}` to your base
template in order to ensure that the Javascript helper is available to you when you need it:

.. code-block:: html

    {% load js_routes_tags %}
    <html>
        <head>
        </head>
        <body>
            <-- At the bottom of the document's body... -->
            {% js_routes %}
        </body>
    </html>

Usage
=====

The URL patterns you configured through the ``JS_ROUTES_INCLUSION_LIST`` setting can then be
reversed using the generated ``window.reverseUrl`` function, which can be used pretty much the
"same" way you'd use `reverse <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_ on
the Django side:
.. code-block:: javascript

    const url1 = window.reverse('home');
    const url2 = window.reverse('catalog:product_list');
    const url3 = window.reverse('catalog:product_detail', productId);
    const url4 = window.reverse('catalog:product_detail', { pk: productId });

Settings
========

JS_ROUTES_INCLUSION_LIST
------------------------

Default: ``[]``

The ``JS_ROUTES_INCLUSION_LIST`` setting allows to define the URL patterns and URL namespaces that
should be exposed to the client side through the generated Javascript helper.

License
=======

MIT. See ``LICENSE`` for more details.

.. _pip: https://github.com/pypa/pip
