from django_ical.views import ICalFeed
from geoevent.models import Event

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    method = 'meeting request'
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def items(self):
        events = Event.objects.filter(approved=True, event_type__event_type__iexact='Internship').order_by('-dstart')
        #print(events)
        return events

    def item_title(self, item):
        print("TITLE:", item.title)
        return item.title

    def item_description(self, item):
        print("DESCRIPTION:", item.description)
        return item.description

    def item_start_datetime(self, item):
        print("DATE_START:")
        from django.utils import timezone
        return timezone.now()

    def item_end_datetime(self, item):
        from django.utils import timezone
        return timezone.now()
    #    return item.dend


    def item_link(self, item):
        return item.url

    def item_guid(self, item):
        return item.uid

    def item_created(self,item):
        return item.created

    #def item_timestamp(self,item):
    #    return item.last_modified

    #def item_modified(self,item):
    #    return item.last_modified

    #def item_class(self,item):
    #    return 'PUBLIC'

    #def item_updateddate(self,item):
    #    return item.last_modified

    def item_location(self,item):
        return item.location

    def item_geolocation(self,item):
        return (item.lat, item.lon)

    #def item_transparency(self,item):
    #    return "TRANSPARENT"

    #def item_organizer(self,item):
    #    return "foo@example.com"
