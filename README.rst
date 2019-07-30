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

Advanced features
=================

Inserting only the serialized URLs in Django templates
------------------------------------------------------

By default, the ``{% js_routes %}`` template tag only allows to trigger the generation of the
serialized URLs (which are stored in a Javascript object on the ``window`` object) and to include a
Javascript URL resolver function in your HTML using the Django's
`static <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#static>`_ template tag.
Actually, a standard use of the ``{% js_routes %}`` statement is equivalent to:

.. code-block:: html

    {% js_routes include_routes_only=True %}
    <script src="{% static 'js/routes/resolver.js' %}"></script>

The ``include_routes_only`` allows to only include the serialized URLs in the output of
``{% js_routes %}``. It gives you the ability to include the Javascript URL resolver that comes with
Django-js-routes using another ``static`` statement. This also allows you to cache the output of
``{% js_routes %}`` if you want.

Dumping the Javascript routes resolver
--------------------------------------

As explained earlier, the ``{% js_routes %}`` template tag triggers the generation of the serialized
URLs and includes a client-side URL resolver in the final HTML. One inconvenient with this behaviour
is that the serialized URLs need to be generated every time your HTML template is rendered.

Instead it is possible to just dump the whole list of serialized URLs and the URL resolver function
to a single Javascript module file. This can be achieved using the ``dump_routes_resolver`` command,
which can be used as follows:

.. code-block:: shell

    $ python manage.py dump_routes_resolver --format=default --output=my_exported_resolver.js

The ``--output`` option allows to specify in which file the serialized routes and resolver function
should be saved while the ``--format`` option allows to specify the Javascript format to use.

``--format`` accepts the following values:

* ``default`` include the routes as a Javascript object that is associated to the ``window`` object
  while the URL resolver is available through the ``window.reverseUrl`` function (which is similar
  to the behaviour provided by the ``{% js_routes %}`` template tag)
* ``es6`` allows to save the routes and the URL resolver as an ES6 module where the ``reverseUrl``
  is the default export

License
=======

MIT. See ``LICENSE`` for more details.

.. _pip: https://github.com/pypa/pip
