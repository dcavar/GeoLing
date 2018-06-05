from django.core.management.base import BaseCommand, CommandError

import sys

from geoevent.parse_vcards import parseVcard

class Command(BaseCommand):
    help = 'Import the information from vcard feed'

    def add_arguments(self, parser):
        parser.add_argument('feed', nargs='+', type=str)

    def handle(self, *args, **options):
        for feed in options['feed']:
            try:
                print("FEED:" + feed)
                # TODO:
                # These are hard-coded for now since we are only importing from
                # LL calcard server.
                # TODO: add your login and password for the CardDAV server here
                user = ""
                passwd = ''
                parseVcard(feed=feed, user=user, passwd=passwd)
            except:
                print(sys.exc_info()[0])


