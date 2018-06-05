"""
urls.py

Authors:
- Damir Cavar <damir@linguistlist.org>
- Lwin Moe <lwin@linguistlist.org>

"""

from django.urls import include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    #re_path(r'^admin/', include(admin.site.urls)),
    re_path(r'^', include('geoevent.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    re_path(r'^accounts/login/$',auth_views.login,
        {'template_name': 'profiles/login.html'}, name='profile_login'),
    re_path(r'^accounts/password/change/$', auth_views.password_change,
        {'template_name': 'profiles/password_change_form.html'}, name='password_change'),
    re_path(r'^accounts/password/change/done/$', auth_views.password_change_done,
        {'template_name': 'profiles/password_change_done.html'}, name='password_change_done'),
    re_path(r'^accounts/password/reset/$', auth_views.password_reset,
        {'template_name': 'profiles/password_reset.html'}, name='password_reset'),
    re_path(r'^accounts/password/reset/done/$', auth_views.password_reset_done,
        {'template_name': 'profiles/password_reset_done.html'}, name='password_reset_done'),
    re_path(r'^accounts/password/reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'profiles/password_reset_complete.html'}, name='password_reset_complete'),
    re_path(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'template_name': 'profiles/password_reset_confirm.html'}, name='password_reset_confirm'),

    re_path(r'^admin/', admin.site.urls),

    # robots.txt
    re_path(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file")

    #re_path(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':False}),
]

#urlpatterns += staticfiles_urlpatterns()
