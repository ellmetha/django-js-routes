django-js-routes
################

.. image:: https://img.shields.io/pypi/l/django-js-routes.svg
    :target: https://pypi.python.org/pypi/django-js-routes/
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/django-js-routes.svg
    :target: https://pypi.python.org/pypi/django-js-routes

.. image:: https://img.shields.io/pypi/v/django-js-routes.svg
    :target: https://pypi.python.org/pypi/django-js-routes/
    :alt: Latest Version

.. image:: https://img.shields.io/travis/ellmetha/django-js-routes.svg
    :target: https://travis-ci.org/ellmetha/django-js-routes
    :alt: Build status

.. image:: https://img.shields.io/codecov/c/github/ellmetha/django-js-routes.svg
    :target: https://codecov.io/github/ellmetha/django-js-routes
    :alt: Codecov status

|

**Django-js-routes** is a Django application allowing to expose and perform reverse lookups of
Django named URL patterns on the client side.

.. contents:: Table of Contents
    :local:

Main requirements
=================

Python 3.5+, Django 2.0+.

Installation
============

To install Django-js-routes, please use the pip_ command as follows:

.. code-block:: shell

    $ pip install django-js-routes

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

Once the list of URLs to expose is configured, you can add the ``{% js_routes %}`` tag to your base
template in order to ensure that the Javascript helper is available to you when you need it:

.. code-block:: html

    {% load js_routes_tags %}
    <html>
        <head>
        </head>
        <body>
            <!-- At the bottom of the document's body... -->
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

    window.reverseUrl('home');
    window.reverseUrl('catalog:product_list');
    window.reverseUrl('catalog:product_detail', productId);
    window.reverseUrl('catalog:product_detail', { pk: productId });

Settings
========

JS_ROUTES_INCLUSION_LIST
------------------------

Default: ``[]``

The ``JS_ROUTES_INCLUSION_LIST`` setting allows to define the URL patterns and URL namespaces that
should be exposed to the client side through the generated Javascript helper.

Advanced features
=================

Inserting only the serialized URLs in Django templates
------------------------------------------------------

By default, the ``{% js_routes %}`` template tag only allows to trigger the generation of the
serialized URLs (which are stored in a Javascript object on the ``window`` object) and to include a
Javascript URL resolver function in your HTML using the Django's
`static <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#static>`_ template tag.
Actually, a standard use of the ``{% js_routes %}`` statement is equivalent to:

.. code-block:: html

    {% js_routes routes_only=True %}
    <script src="{% static 'js/routes/resolver.js' %}"></script>

The ``routes_only`` option allows to only include the serialized URLs in the output of
``{% js_routes %}``. It gives you the ability to include the Javascript URL resolver that comes with
Django-js-routes using another ``static`` statement. This also allows you to cache the output of the
``{% js_routes routes_only=True %}`` statement if you want (so that serialized URLs are not
generated for every request).

Dumping the Javascript routes resolver
--------------------------------------

As explained earlier, the ``{% js_routes %}`` template tag triggers the generation of the serialized
URLs and includes a client-side URL resolver in the final HTML. One downside of this behaviour is
that the serialized URLs need to be generated every time your HTML template is rendered.

Instead it is possible to just dump the whole list of serialized URLs AND the URL resolver function
into a single Javascript module file. This can be achieved using the ``dump_routes_resolver``
command, which can be used as follows:

.. code-block:: shell

    $ python manage.py dump_routes_resolver --format=default --output=my_exported_resolver.js

The ``--output`` option allows to specify to which file the serialized routes and resolver function
should be saved while the ``--format`` option allows to specify the Javascript format to use.

``--format`` accepts the following values:

* ``default`` includes the routes as an object that is associated to the ``window`` object while the
  URL resolver is available through the ``window.reverseUrl`` function (this corresponds to the
  behaviour provided by a standard use of the ``{% js_routes %}`` template tag)
* ``es6`` allows to save the routes and the URL resolver as an ES6 module where the ``reverseUrl``
  function is the default export

License
=======

MIT. See ``LICENSE`` for more details.

.. _pip: https://github.com/pypa/pip
