from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from geoevent.models import Event, Profile, EventType

'''
class EventForm(forms.Form):
    type = forms.ModelChoiceField(queryset=EventType.objects.filter(event_type='Event'), label=_('Post Type'), empty_label=None, required=False)
    # if we want to enable all types from the database, use the following instead of the above
    #type = forms.ModelChoiceField(queryset=EventType.objects.all(), label=_('Post Type'),empty_label=None, required=False)

    title = forms.CharField(max_length=300, label=_('Title'), required=True)
    description = forms.CharField(required=False, label=_('Description'),
                                widget = forms.Textarea(attrs={'rows':10, 'cols':40}))
    url = forms.URLField(required=False, label=_('URL'))
    dstart = forms.DateTimeField(('%Y-%m-%d %H:%M',), label=_('Start Date/Time'), required=False,
                                widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M',
                                attrs={'class':'datetimepicker'}))
    dend = forms.DateTimeField(('%Y-%m-%d %H:%M',), label=_('End Date/Time'), required=False,
                                widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M',
                                attrs={'class':'datetimepicker'}))
    due = forms.DateTimeField(('%Y-%m-%d %H:%M',), label=_('Deadline'), required=False,
                                widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M',
                                attrs={'class':'datetimepicker'}))
    location = forms.CharField(label='Location', widget = forms.Textarea(attrs={'rows':4, 'cols':40}),
                               required=True)
'''

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_type', 'title', 'description', 'url', 'dstart', 'dend', 'due', 'location',]
        widgets = {
            'dstart': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class': 'datetimepicker'}),
            'dend': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class': 'datetimepicker'}),
            'due': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class': 'datetimepicker'}),
            'location': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }

class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'localization', 'lat', 'lon', 'tos_accepted', 'banned', 'verified',)
        #fields = ('display_user_name')


# vcard form
# URL:http://www.brown.edu/Departments/CLPS/
# N:University;Brown;;;
# FN:Brown University
# ADR;TYPE=WORK:Box 1821;;190 Thayer Street;Providence;RI;02912;United States
# ORG:Brown University;Department of Cognitive\, Linguistic\, & Psychological Sciences;
# KIND:organization
# CATEGORIES:LINGUISTICS,ACADEMIC,EDUCATION
# TITLE:
# ROLE:
# NOTE:
# FBURL:
# LABEL;TYPE=WORK:190 Thayer Street\nProvidence\, RI\n02912\nBox 1821\nUnited States
# EMAIL;TYPE=OTHER:CLPS@brown.edu
# TEL;TYPE=WORK,VOICE:+1 401 863-2727
# TEL;TYPE=WORK,FAX:+1 401 863-2255