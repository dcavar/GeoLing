from django.contrib.auth.models import User

#from dateutil.parser import parse
import geocoder
import requests
from icalendar import Calendar, vDatetime, vDate, vDDDTypes

from geoevent.models import Event, EventType

def parseFeed(feed, event_type):
    #f = '%Y-%m-%d %H:%M:%S+00:00'
    cal = requests.get(feed)
    cal.encoding = "utf-8"
    gcal = Calendar.from_ical(cal.text)
    for component in gcal.walk():
        location = ''
        #last_modified = ''
        summary = ''
        event = None
        uid = None

        if component.name == "VEVENT":
            user = User.objects.get(id=1)
            #print(user)
            event_type = EventType.objects.get(event_type=event_type)
            #print(event_type)

            if component.get('uid'):
                uid = component.get('uid')

            try:
                lookupEvent = Event.objects.get(uid=uid)
                #lookupEvent = Event.objects.get(title=event.title, description=event.description, url=event.url, dstart=event.dstart, dend=event.dend, due=event.due, location=event.location)
                print("Found an existing event and updating it.")
            except Event.DoesNotExist:
                lookupEvent = None
            except Event.MultipleObjectsReturned:
                print("Found multiple objects. Skipping. Check: " + summary)
                continue

            # if the event already exists
            if lookupEvent:
                event = lookupEvent
            else: # otherwise, create a new one
                event = Event()

            if uid:
                print('UID: ' + uid)
                event.uid = uid

            if component.get('dtstart'):
                dtstart = component.get('dtstart')
                dtstart = str(vDDDTypes.from_ical(dtstart))
                #print("Date Start:" + dtstart)
                        # format f is defined at the top of the function
                event.dstart = dtstart

            if component.get('dtend'):
                dtend = component.get('dtend')
                dtend = str(vDDDTypes.from_ical(dtend))
                #print('Date End: ' + dtend)
                event.dend = dtend

            if component.get('dtstamp'):
                dtstamp = component.get('dtstamp')
                dtstamp = str(vDDDTypes.from_ical(dtstamp))
                #print('Date Stamp: ' + dtstamp)

            if component.get('created'):
                created = component.get('created')
                created = str(vDDDTypes.from_ical(created))
                #print('Date Created: ' + created)

            if component.get('due'):
                due = component.get('due')
                due = str(vDDDTypes.from_ical(due))
                #print('Date Due: ' + due)
                event.due = due

            if component.get('summary'):
                summary = component.get('summary')
                #print('Summary: ' + summary)
                event.title = summary

            if component.get('description'):
                description = component.get('description')
                #print('Description: ' + description)
                event.description = description

            if component.get('url'):
                url = component.get('url')
                #print('URL: ' + url)
                event.url = url

            if component.get('location'):
                location = component.get('location')
                #print('Location: ' + location)
                event.location = location

            if component.get('geo'):
                geo = component.get('geo')
                event.lat = geo.latitude
                event.lon = geo.longitude
            else:
                if component.get('location'):
                    geocode = geocoder.google(location)
                    event.lat = geocode.lat
                    event.lon = geocode.lng
                    #print ('Geo Code: ' + str(geocode.lat) + ' , ' + str(geocode.lng))

            if component.get('related-to'):
                related_to = component.get('related-to')
                #print('RELATED-TO: ' + related_to)
                event.related_to = related_to

            #if component.get('last-modified'):
            #    last_modified = component.get('last-modified')
            #    event.last_modified = vDDDTypes.from_ical(last_modified)
            #    print('LAST-MODIFIED: ' + str(vDDDTypes.from_ical(last_modified)))

            event.user = user
            event.event_type = event_type
            event.approved = True

            #print("Saving...")
            event.save()
            print("================================")
    cal.close()