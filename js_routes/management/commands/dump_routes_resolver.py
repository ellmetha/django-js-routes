"""
    Django JS Routes resolver dump command
    ======================================

    This command allows to export a JS module containing the Django URLs that should be exposed on
    the client side as of a resolver helper allowing to perform URL lookups.

"""

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from js_routes.serializers import url_patterns_serializer


class Command(BaseCommand):
    """ Dumps Django URLs and the resolver helper in a single JS file. """

    help = 'Dump Django URLs and the resolver helper in a single JS file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            default='default',
            choices=['default', 'es6'],
            help='Specifies the format of the generated URL resolver helper.',
        )
        parser.add_argument(
            '-o', '--output',
            help='Specifies a file to which the output is written.'
        )

    def handle(self, *args, **options):
        """ Performs the command actions. """
        output = open(options['output'], 'w') if options['output'] else self.stdout
        output.write(
            render_to_string(
                'js_routes/_dump/{}.js'.format(options['format']),
                {'routes': url_patterns_serializer.to_json()}
            )
        )
