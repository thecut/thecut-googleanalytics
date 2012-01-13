# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from thecut.googleanalytics import settings
from thecut.googleanalytics.managers import ProfileManager


class Profile(models.Model):
    """Google Analytics profile settings for a site.
    
    Google Analytics profiles can be created at:
    http://www.google.com/analytics/
    
    """
    site = models.OneToOneField('sites.Site', unique=True, related_name='+')
    web_property_id = models.CharField('web property ID', max_length=25,
        help_text='Web Property ID is obtained when ' \
        '<a href="http://www.google.com/analytics/" target="_new">' \
        'configuring the site profile in Google Analytics</a>.')
    profile_id = models.CharField('profile ID', max_length=25, blank=True,
        default='')
    is_enabled = models.BooleanField('enabled', default=False,
        help_text='Is Google Analytics tracking enabled on the website?')
    # gdata.gauth.OAuth2Token blob
    _oauth2_token = models.TextField(default='', blank=True, editable=False)
    objects = ProfileManager()
    
    class Meta(object):
        ordering = ['site']
    
    def __unicode__(self):
        return self.site.name
    
    def get_gdata_client(self):
        assert self.use_gdata()
        from gdata.analytics.client import AnalyticsClient
        if not hasattr(self, '_gdata_client'):
            self._gdata_client = AnalyticsClient(source=settings.USER_AGENT)
            self.oauth2_token.authorize(self._gdata_client)
        return self._gdata_client
    
    def use_gdata(self):
        return bool(self._oauth2_token and settings.USE_GDATA)
    
    @property
    def oauth2_token(self):
        from gdata.gauth import OAuth2Token, token_from_blob
        return self._oauth2_token and token_from_blob(self._oauth2_token) \
            or None
    
    @oauth2_token.setter
    def oauth2_token(self, oauth2_token):
        from gdata.gauth import OAuth2Token, token_to_blob
        if type(oauth2_token) is OAuth2Token:
            self._oauth2_token = token_to_blob(oauth2_token)
        elif oauth2_token is None:
            self._oauth2_token = ''
        else:
            raise TypeError('Expected type OAuth2Token or None')
    
    def revoke_oauth2_token(self):
        client = self.get_gdata_client()
        client.revoke_token()
        self.oauth2_token = None

