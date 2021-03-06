# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings, views
from .forms import GoogleAPIProfileAdminForm, ProfileAdminForm
from .models import Profile
from django.contrib import admin

try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'web_property_id', 'profile_id',
                    'is_enabled', 'linked')

    def linked(self, obj):
        if settings.USE_GOOGLE_API:
            if obj.use_google_api():
                label = 'Linked (<a href="oauth2/revoke/{0}">unlink</a>)'
            else:
                label = 'Unlinked (<a href="oauth2/request/{0}">link</a>)'
            return label.format(obj.pk)
        else:
            return 'Disabled'
    linked.allow_tags = True
    linked.short_description = 'Analytics API'

    def get_form(self, request, obj=None, **kwargs):
        # Calling super didn't work with Django 1.6, so we're just returning
        # the ModelForm class.
        if obj and obj.use_google_api():
            return GoogleAPIProfileAdminForm
        else:
            return ProfileAdminForm

    def get_urls(self):
        urlpatterns = patterns(
            'thecut.googleanalytics.views',

            url(r'^oauth2/request/(?P<pk>\d+)$',
                views.OAuth2RequestTokenView.as_view(),
                name='oauth2_request_token'),
            url(r'^oauth2/callback$',
                views.OAuth2CallbackView.as_view(),
                name='oauth2_callback'),
            url(r'^oauth2/revoke/(?P<pk>\d+)$',
                views.OAuth2RevokeTokenView.as_view(admin=self),
                name='oauth2_revoke_token'),
        )
        urlpatterns += super(ProfileAdmin, self).get_urls()
        return urlpatterns

admin.site.register(Profile, ProfileAdmin)
