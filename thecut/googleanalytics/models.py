# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import receivers, settings
from .managers import ProfileManager
from googleapiclient.discovery import build
from django.db import models
from httplib2 import Http
from oauth2client.django_orm import CredentialsField, Storage


# South introspection rules for oauth2client's CredentialsField
try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules(
        [], ['^oauth2client\.django_orm\.CredentialsField'])


class Profile(models.Model):
    """Google Analytics profile settings for a site.

    Google Analytics profiles can be created at:
    http://www.google.com/analytics/

    """

    site = models.OneToOneField('sites.Site', unique=True, related_name='+')

    web_property_id = models.CharField(
        'property tracking ID', max_length=25,
        help_text='The property tracking ID is available when viewing the '
                  '"Tracking Code" details in the Google Analytics admin.')

    profile_id = models.CharField('view (profile) ID', max_length=25,
                                  blank=True, default='')

    display_features = models.BooleanField(
        'Use Display advertising features?', default=False,
        help_text='Used for remarketing, demographics and interest reporting.')

    is_enabled = models.BooleanField(
        'enabled', default=False, help_text='Is Google Analytics tracking '
                                            'enabled on the website?')

    objects = ProfileManager()

    class Meta(object):
        ordering = ['site']
        verbose_name = 'view (profile)'
        verbose_name_plural = 'views (profiles)'

    def __unicode__(self):
        return self.site.name

    def _get_oauth2_storage(self):
        return Storage(ProfileOAuth2Credentials, 'id', self, 'credentials')

    def get_analytics_google_api_client(self):
        if self.use_google_api():
            http = self.oauth2_credentials.authorize(Http())
            return build('analytics', 'v3', http=http)
        else:
            # TODO
            raise Exception('Google API not available.')

    def use_google_api(self):
        if (self.pk and settings.USE_GOOGLE_API):
            return ProfileOAuth2Credentials.objects.filter(id=self).exists()
        else:
            return False

    @property
    def oauth2_credentials(self):
        storage = self._get_oauth2_storage()
        return storage.get()

    @oauth2_credentials.setter
    def oauth2_credentials(self, credentials):
        storage = self._get_oauth2_storage()
        return storage.put(credentials)

models.signals.post_save.connect(receivers.clear_cache, sender=Profile)
models.signals.post_delete.connect(receivers.clear_cache, sender=Profile)


class ProfileOAuth2Credentials(models.Model):
    """Stores Google OAuth2 credentials for a Profile."""

    # Very yucky to use the id like this, but it is required by oauth2client's
    # django_orm Storage, which blindly created new instances without checking
    # to see if one already exists - with an id, it gets saved over the top).
    id = models.OneToOneField('googleanalytics.Profile',
                              related_name='_oauth2_credentials',
                              primary_key=True)
    credentials = CredentialsField()

models.signals.post_save.connect(receivers.clear_cache,
                                 sender=ProfileOAuth2Credentials)
models.signals.post_delete.connect(receivers.clear_cache,
                                   sender=ProfileOAuth2Credentials)
