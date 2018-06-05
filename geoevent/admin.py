from django.contrib import admin
from .models import Profile, Event, EventType, Address
from .models import Contact, Adr, Adr_type, Email, Email_type, Nickname, Label, Org, Role, Tel, Tel_type, URL

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)

class EventAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('event_type', 'approved')

class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ('event_type',)

class AddressAdmin(admin.ModelAdmin):
    pass



#vcard models
class Adr_typeInline(admin.StackedInline):
    model = Adr_type
    extra = 1
class AdrAdmin(admin.ModelAdmin):
    inlines = [Adr_typeInline]
    extra = 1
class AdrInline(admin.StackedInline):
    model = Adr
    extra = 1
class EmailInline(admin.StackedInline):
    model = Email
    extra = 1
class NicknameInline(admin.StackedInline):
    model = Nickname
    extra = 1
class LabelInline(admin.StackedInline):
    model = Label
    extra = 1
class OrgInline(admin.StackedInline):
    model = Org
    extra = 1
class RoleInline(admin.StackedInline):
    model = Role
    extra = 1
class TelInline(admin.StackedInline):
    model = Tel
    extra = 1
class URLInline(admin.StackedInline):
    model = URL
    extra = 1
class ContactAdmin(admin.ModelAdmin):
    search_fields = ('fn','n',)
    inlines = [
        AdrInline,
        EmailInline,
        LabelInline,
        NicknameInline,
        OrgInline,
        RoleInline,
        TelInline,
        URLInline,
    ]


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Address, AddressAdmin)

admin.site.register(Contact, ContactAdmin)
admin.site.register(Adr, AdrAdmin)
