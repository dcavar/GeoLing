from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from geoling import settings
import geocoder

from geoevent.models import EventType, Event, Profile, Contact, Adr
from geoevent.forms import UserForm, ProfileForm, NewUserForm, EventForm

def handler_500(request):
    r = render(request, '500.html')
    r.status_code = 500
    return r

def handler_404(request):
    r = render(request, '404.html')
    r.status_code = 404
    return r

@xframe_options_exempt
def index(request):
    '''Possible values for type are: event,job,conference,internship,summerschool,contact,language'''
    type = request.GET.get('type', 'event') # the default is 'event'
    types = type.split(',')
    return render(request, 'geoevent/map.html', {'types': types})
    return render(request, 'geoevent/map.html',{})

def map(request):
    '''Possible values for type are: event,job,conference,internship,summerschool,contact,language'''
    type = request.GET.get('type', '')
    types = type.split(',')
    return render(request, 'geoevent/map.html',{'types': types})

def map_new(request):
    return render(request, 'geoevent/map_new.html', {})

def details(request, id):
    event = get_object_or_404(Event, approved=True, pk=id)
    return render(request, 'geoevent/detail.html',{'event': event,})

def continfo(request, uid):
    cont = get_object_or_404(Contact, uid=uid)
    return render(request, 'geoevent/continfo.html',{'cont': cont,})

# cache page for 15 mins
@cache_page(60 * 15)
def generate_kml(request, type, format):
    '''
    NOTE: format argument is for the future handling of other formats, e.g. json
    It only handles KML for now
    '''

    # a special case for languages
    if type == 'language' and format == 'kml':
        return render(request, 'geoevent/language.kml',{})

    # a special case for contacts
    if type == 'contact' and format == 'kml':
        return render(request, 'geoevent/contacts.kml',{'contacts':Contact.objects.all()})

    # check if the event_type exists in the database
    try:
        EventType.objects.get(event_type__iexact=type)
    except EventType.DoesNotExist:
        return HttpResponse(status=404)

    # get all the events of "type" (from the argument), with dstart greater than or equal
    # to today
    #from datetime import date
    from django.utils import timezone
    events = Event.objects.filter(event_type__event_type__iexact=type).filter(approved=True).filter(dend__gte=timezone.now())

    # if the return format is KML
    if format == 'kml':
        return render(request, 'geoevent/data.kml',{'events':events,})
    elif format == 'rss':
        # we only want the last 10 entries
        events = events.order_by('-last_modified')[:10]
        return render(request, 'geoevent/rss.xml',{'events':events, 'type':type})
    elif format == 'alexa':
        # we only want the last 10 entries
        events = events.order_by('-last_modified')[:10]
        return render(request, 'geoevent/alexa.xml',{'events':events, 'type':type})
    else:
        return HttpResponse(status=404)

def adduser(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        gRecaptchaRes = request.POST.get(u'g-recaptcha-response', None)
        if form.is_valid() and gRecaptchaRes != None:
            values = {
                'secret': settings.RECAPTCHA_PRIVATE,
                'response': gRecaptchaRes,
                'remoteip': request.META.get("REMOTE_ADDR", None),
            }
            import urllib.request
            import urllib.parse
            import json
            params = urllib.parse.urlencode(values)
            url = settings.RECAPTCHA_API + '?%s' % params
            with urllib.request.urlopen(url) as f:
                response_data = f.read().decode('utf-8')
                json_data = json.loads(response_data)
                if json_data['success']:
                    new_user = User.objects.create_user(**form.cleaned_data)
                    new_user.save()
                    profile = Profile()
                    profile.user = new_user
                    profile.save()
                    user = authenticate(username=request.POST['username'], password=request.POST['password'])
                    #if user is not None:
                        # the password verified for the user
                    #    if user.is_active:
                    #        print("User is valid, active and authenticated")
                    #        login(request, user)
                    login(request, user)
                    return HttpResponseRedirect('/accounts/profile/')
    else:
        form = NewUserForm()
    return render(request, 'profiles/adduser.html', {
        'form': form,
        'recaptcha_pub': settings.RECAPTCHA_PUBLIC})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            #return render(request, 'profiles/profile.html',
            #              {'user_form': user_form,
            #               'profile_form': profile_form,
            #               }, context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            user = request.user
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=user.profile)
    return render(request, 'profiles/profile.html',
            {'user_form': user_form,
             'profile_form': profile_form,
            })

'''
@login_required
def add_event(request):
    if request.method == 'POST': # If the form has been submitted...
        form = EventForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            title = form.cleaned_data['title'] or None
            description = form.cleaned_data['description'] or None
            url = form.cleaned_data['url'] or None
            dstart = form.cleaned_data['dstart'] or None
            dend = form.cleaned_data['dend'] or None
            due = form.cleaned_data['due'] or None
            location = form.cleaned_data['location'] or None
            type = form.cleaned_data['type'] or None

            event = Event()
            event.title = title
            if description:
                event.description = description
            if url:
                event.url = url
            if dstart:
                event.dstart = dstart
            if dend:
                event.dend = dend
            if due:
                event.due = due
            if location:
                event.location = location
                g = geocoder.google(location)
                if g.lat:
                    event.lat = g.lat
                if g.lng:
                    event.lon = g.lng
            if type:
                event.event_type = type

            if request.user.is_authenticated():
                event.user = request.user
            event.save()
            return render(request, 'geoevent/thanks.html',{ })
    else:
        form = EventForm() # An unbound form
    return render(request, 'geoevent/event_form.html', {
        'form': form,
      }
    )
'''

@login_required
def update_event(request, id=None):
    if id:
        instance = get_object_or_404(Event, id=id, user=request.user)
    else:
        instance = None
    form = EventForm(request.POST or None, instance=instance)

    # if we want to enable all types from the database, comment this out
    if not id:
        form.fields["event_type"].queryset = EventType.objects.filter(event_type='Event')

    if form.is_valid():
        event = form.save()
        if event.location:
            g = geocoder.google(event.location)
            if g.lat:
                event.lat = g.lat
            if g.lng:
                event.lon = g.lng
        if request.user.is_authenticated():
            event.user = request.user
        event.approved = False
        event.save()

        message = "Please approve a submitted event at GeoLing.\n"
        message += "Event Title:" + event.title + "\n"
        submitter = ''
        if event.user.first_name or event.user.last_name:
            submitter = event.user.first_name + " " + event.user.last_name
        else:
            submitter = event.user.username
        message += "Submitter:" + submitter + "\n"
        from dateutil import tz
        to_zone = tz.gettz('America/Indianapolis')
        est = event.last_modified.astimezone(to_zone)
        message += "Date:" + est.strftime("%Y-%m-%d %H:%M")
        from django.core.mail import EmailMessage
        # subject, message body, from, to, bcc, reply_to
        # Please don't forget to set email credentials in secret.py
        email = EmailMessage(
            'Local event submitted',
            message,
            'noreply@linguistlist.org',
            ['form@linguistlist.org'],
            [],
            reply_to=['noreply@linguistlist.org'],
        )
        email.send()

        return render(request, 'geoevent/thanks.html', {})
    return render(request, 'geoevent/event_form.html', {'form': form,})

@login_required
def user_submissions(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'profiles/submissions.html', {'events':events,})

def icalendar(request, type):
    url = 'geoevent/' + type + '.ics'
    return render(request, url,{})

def howto(request):
    return render(request, 'geoevent/howto.html')
