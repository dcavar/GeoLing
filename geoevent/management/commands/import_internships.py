from django.core.management.base import BaseCommand, CommandError

import sys

from geoevent.read_ical import parseFeed

class Command(BaseCommand):
    help = 'Import the information from ical feed'

    def add_arguments(self, parser):
        parser.add_argument('feed', nargs='+', type=str)

    def handle(self, *args, **options):
        for feed in options['feed']:
            try:
                print("FEED:" + feed)
                type = 'Internship'
                parseFeed(feed=feed, event_type=type)
            except:
                print(sys.exc_info()[0])