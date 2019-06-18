# -*- coding: utf-8 -*-

import codecs
from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup

import js_routes


def read_relative_file(filename):
    """ Returns contents of the given file, whose path is supposed relative to this module. """
    with codecs.open(join(dirname(abspath(__file__)), filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='django-js-routes',
    version=js_routes.__version__,
    author='Morgan Aubert',
    author_email='me@morganaubert.name',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ellmetha/django-js-routes',
    license='BSD',
    description='Expose and perform reverse lookups of Django URLs in the frontend world.',
    long_description=read_relative_file('README.rst'),
    keywords='django urls reverse routes resolution frontend js javascript export',
    zip_safe=False,
    install_requires=[
        'django>=2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
