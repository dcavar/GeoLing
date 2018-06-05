from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
import geocoder

class Location(models.Model):
    event = models.ForeignKey('Event', related_name="locations", on_delete = models.DO_NOTHING)
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lng = models.FloatField(_('Longitude'), blank=True, null=True)
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Label'))

    def __str__(self):
        return self.url

class EventType(models.Model):
    event_type = models.CharField(max_length=20)

    def __str__(self):
        return self.event_type

class Event(models.Model):
    user = models.ForeignKey(User, related_name="events", null=True, on_delete = models.DO_NOTHING)
    title = models.CharField(max_length=500, verbose_name=_('Title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'), help_text='You can use Markdown syntax for formatting: https://daringfireball.net/projects/markdown/syntax')
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lon = models.FloatField(_('Longitude'), blank=True, null=True)
    location = models.TextField(verbose_name=_('Local Address'), help_text='Please put in the address of the event so that your event will show up on the map.')
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    due = models.DateTimeField(blank=True, null=True, verbose_name=_('Due Date'))
    dstart = models.DateTimeField(blank=True, null=True, verbose_name=_('Start Date'))
    dend = models.DateTimeField(blank=True, null=True, verbose_name=_('End Date'))
    uid = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('UID'))
    related_to = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('RELATED-TO'))
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    event_type = models.ForeignKey(EventType, related_name="event", null=True, on_delete = models.DO_NOTHING)

    approved = models.BooleanField(default=False, blank=True, verbose_name=_('Approved'))
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def geolocation(self):
        geolocation = (self.lat, selt.lon)
        return geolocation

    def setLatLon(self):
        if self.location:
            g = geocoder.google(self.location)
            if g.lat:
                self.lat = g.lat
            if g.lng:
                self.lon = g.lng

'''
class DateType(models.Model):
    date_type = models.CharField(max_length=125)

    def __str__(self):
        return self.date_type
'''

'''
class Date(models.Model):
    event = models.ForeignKey(Event)
    date_type = models.ForeignKey(DateType)
    date_time = models.DateTimeField()
'''

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete = models.DO_NOTHING)
    display_user_name = models.CharField(max_length=255, blank=True, null=True)
    avatar_url = models.CharField(max_length=200, blank=True, default='')
    localization = models.CharField(max_length=10, default='en')
    url = models.URLField(blank=True, null=True, verbose_name=_('URL'))
    show = models.BooleanField(default=False, blank=True, verbose_name=_('Show'))

    # the followings will be replaced by ManyToManyField
    #location = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('Address'))
    #lat = models.FloatField(_('Latitude'), blank=True, null=True)
    #lon = models.FloatField(_('Longitude'), blank=True, null=True)

    #addresses = models.ManyToManyField(Address, related_name="profiles")

    banned = models.BooleanField(default=False, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    tos_accepted = models.BooleanField(default=False)

    # institution profiles will have to be verified/approved
    institution = models.BooleanField(default=False, blank=True)

    #verified? (to be able to submit feeds)
    verified = models.BooleanField(default=False, blank=True)

    bio = models.TextField(_('BIO'), blank=True)
    specialization = models.CharField(_('Specialization'), max_length=150, blank=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    #profile = models.ForeignKey('Profile', related_name="addresses")
    profiles = models.ManyToManyField(Profile, related_name="addresses")
    location = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('Address'))
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lng = models.FloatField(_('Longitude'), blank=True, null=True)
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Label'))

    def __str__(self):
        return self.url



#classes for importing vcards

class Contact(models.Model):
    fburl = models.CharField(max_length=2000, blank=True, null=True)
    fn = models.CharField(max_length=2000, blank=True, null=True)
    n = models.CharField(max_length=2000, blank=True, null=True)
    kind = models.CharField(max_length=2000, blank=True, null=True)
    prodid = models.CharField(max_length=2000, blank=True, null=True)
    uid = models.CharField(max_length=2000, blank=True, null=True)
    version = models.CharField(max_length=2000, blank=True, null=True)

    x_ablabel = models.CharField(max_length=2000, blank=True, null=True)
    x_abuid = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_assistant = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_blog_url = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_file_as = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_manager = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_spouse = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_video_url = models.CharField(max_length=2000, blank=True, null=True)
    x_evolution_webdav_href = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_editingstatus = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_editorapproval = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_institutionid = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progalternatename = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progappdeadline = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progdescr = models.TextField(blank=True, null=True)
    x_linguistlist_progdistinctions = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progeditorcomment = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progfinancialaid = models.TextField(blank=True, null=True)
    x_linguistlist_programmid = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progsize = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progspecial = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progstatus = models.CharField(max_length=2000, blank=True, null=True)
    x_linguistlist_progtitle = models.CharField(max_length=2000, blank=True, null=True)
    x_mozilla_html = models.CharField(max_length=2000, blank=True, null=True)
    x_radicale_name = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.fn

class Adr(models.Model):
    contact = models.ForeignKey(Contact, related_name="adrs", on_delete = models.DO_NOTHING)
    post_office_box = models.CharField(max_length=1024, verbose_name=_("post office box"), blank=True)
    extended_address = models.CharField(max_length=1024, verbose_name=_("extended address"), blank=True)
    street_address = models.CharField(max_length=1024, verbose_name=_("street address"))
    locality = models.CharField(max_length=1024, verbose_name=_("locality"))
    region = models.CharField(max_length=1024, verbose_name=_("region"))
    postal_code = models.CharField(max_length=1024, verbose_name=_("postal code"))
    country_name = models.CharField(max_length=1024, verbose_name=_("country name"))
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lon = models.FloatField(_('Longitude'), blank=True, null=True)

    def __str__(self):
        return self.country_name

class Adr_type(models.Model):
    TYPE_CHOICES = (
        ('INTL', _(u"INTL")),
        ('POSTAL', _(u"postal")),
        ('PARCEL', _(u"parcel")),
        ('WORK', _(u"work")),
        ('dom', _(u"dom")),
        ('home', _(u"home")),
        ('pref', _(u"pref")),
    )
    adr = models.ForeignKey(Adr, related_name="adr_types", on_delete = models.DO_NOTHING)
    type = models.CharField(max_length=1024, verbose_name=_("type"), choices=TYPE_CHOICES)



class Email(models.Model):
    contact = models.ForeignKey(Contact, related_name="emails", on_delete = models.DO_NOTHING)
    value = models.EmailField(max_length=100, verbose_name=_("value"))

class Email_type(models.Model):
    TYPE_CHOICES = (
        ('INTERNET', _(u"internet")),
        ('x400', _(u"x400")),
        ('pref', _(u"pref")),
    )

    type = models.CharField(max_length=30, verbose_name=_("type of email"), choices=TYPE_CHOICES)
    email = models.ForeignKey(Email, related_name="email_types", on_delete = models.DO_NOTHING)


class Nickname(models.Model):
    contact = models.ForeignKey(Contact, related_name="nicknames", on_delete = models.DO_NOTHING)
    data = models.CharField(max_length=100, blank=True, null=True)

class Label(models.Model):
    contact = models.ForeignKey(Contact, related_name="labels", on_delete = models.DO_NOTHING)
    data = models.CharField(max_length=2000, blank=True, null=True)

class Org(models.Model):
    contact = models.ForeignKey(Contact, related_name="orgs", on_delete = models.DO_NOTHING)
    organization_name = models.CharField(max_length=1024, verbose_name=_("organization name"))
    organization_unit = models.CharField(max_length=1024, verbose_name=_("organization unit"), blank=True)

class Role(models.Model):
    contact = models.ForeignKey(Contact,related_name="roles", on_delete = models.DO_NOTHING)
    data = models.CharField(max_length=100, blank=True, null=True)

class Tel(models.Model):
    contact = models.ForeignKey(Contact, related_name="tels", on_delete = models.DO_NOTHING)
    value = models.CharField(max_length=100, verbose_name=_("value"))

class Tel_type(models.Model):
    TYPE_CHOICES = (
        ('VOICE', _(u"INTL")),
        ('HOME', _(u"home")),
        ('MSG', _(u"message")),
        ('WORK', _(u"work")),
        ('pref', _(u"prefered")),
        ('fax', _(u"fax")),
        ('cell', _(u"cell phone")),
        ('video', _(u"video")),
        ('pager', _(u"pager")),
        ('bbs', _(u"bbs")),
        ('modem', _(u"modem")),
        ('car', _(u"car phone")),
        ('isdn', _(u"isdn")),
        ('pcs', _(u"pcs")),
    )

    type = models.CharField(max_length=30, verbose_name=_("type of phone number"), help_text=_("for instance WORK or HOME"), choices=TYPE_CHOICES)
    tel = models.ForeignKey(Tel, related_name="tel_types", on_delete = models.DO_NOTHING)
    def __str__(self):
        return self.type

class URL(models.Model):
    contact = models.ForeignKey(Contact, related_name="urls", on_delete = models.DO_NOTHING)
    data = models.TextField()


