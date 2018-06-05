from django.conf.urls import url
from geoevent import views
from geoevent.feeds import EventFeed

from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import views as auth_views

handler500 = 'views.handler_500'
handler404 = 'views.handler_404'

app_name = 'geoevent'

urlpatterns = [
    url(r'^$', views.index, name='geoevent_index'),

    url(r'^add/$', views.update_event, name='add_event'),
    url(r'^update/(?P<id>\d+)/', views.update_event, name='update_event'),

    url(r'^map/$', views.map, name='geoevent_map'),
    url(r'^map_new/$', views.map_new, name='geoevent_map_new'),
    url(r'^submissions/', views.user_submissions, name='user_submissions'),
    url(r'^(?P<id>\d+)/$', views.details, name='event_details'),


    url(r'^data/(?P<format>[\w-]+)/(?P<type>[\w-]+)/$', views.generate_kml, name='generate_kml'),

url(r'^data/(?P<format>[\w-]+)/(?P<type>[\w-]+).xml$', views.generate_kml, name='generate_kml'),

    url(r'^ical/(?P<type>[\w-]+)/$', views.icalendar, name='ical'),

    url(r'^howto/$', views.howto, name='howto'),

    #TODO: the followings can be removed
    #url(r'^events/events.kml$', views.events_kml, name='events_kml'),
    #url(r'^jobs/jobs.kml$', views.jobs_kml, name='jobs_kml'),
    #url(r'^contacts/contacts.kml$', views.contacts_kml, name='contacts_kml'),
    #url(r'^conferences/conferences.kml$', views.conferences_kml, name='conferences_kml'),
    #url(r'^intern/intern.kml$', views.intern_kml, name='intern_kml'),
    #url(r'^summers/summers.kml$', views.summers_kml, name='summers_kml'),
    #url(r'^language/language.kml$', views.language_kml, name='language_kml'),
    # end to be removed

    url(r'^latest/feed.ics$', EventFeed(), name='ical_feed'),

    url(r'^accounts/profile/$', views.profile, name='profile_index'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/register/$', views.adduser, name='add_profile'),

    url(r'^contacts/(?P<uid>.*)$', views.continfo, name='continfo'),

]
