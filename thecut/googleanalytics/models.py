# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from thecut.googleanalytics import settings
from thecut.googleanalytics.managers import AnalyticsWebPropertyManager
import pickle


class AnalyticsWebProperty(models.Model):
    """Google Analytics web property settings for a site.
    
    Google Analytics profiles can be created at:
    http://www.google.com/analytics/
    
    """
    site = models.OneToOneField('sites.Site', unique=True, related_name='+')
    web_property_id = models.CharField(max_length=25,
        help_text='Web Property ID is obtained when \
        <a href="http://www.google.com/analytics/" target="_new">\
        configuring the site profile in Google Analytics</a>.')
    is_enabled = models.BooleanField(default=False,
        help_text='Is Google Analytics tracking enabled on the website?')
    # pickled gdata.gauth.OAuth2Token object
    _oauth2_token = models.TextField(default='', blank=True, editable=False)
    objects = AnalyticsWebPropertyManager()
    
    class Meta(object):
        ordering = ['site']
        verbose_name = 'web property'
        verbose_name_plural = 'web properties'
    
    def __unicode__(self):
        return self.site.name
    
    def get_gdata_client(self):
        assert self.use_gdata()
        from gdata.analytics.client import AnalyticsClient
        if not hasattr(self, '_gdata_client'):
            self._gdata_client = AnalyticsClient()
            self.oauth2_token.authorize(self._gdata_client)
        return self._gdata_client
    
    def use_gdata(self):
        return bool(self._oauth2_token and settings.USE_GDATA)
    
    @property
    def oauth2_token(self):
        # TODO: Only pickle when loading/saving to the database?
        from gdata.gauth import OAuth2Token
        return self._oauth2_token and pickle.loads(str(self._oauth2_token)) \
            or None
    
    @oauth2_token.setter
    def oauth2_token(self, oauth2_token):
        # TODO: Only pickle when loading/saving to the database?
        from gdata.gauth import OAuth2Token
        if type(oauth2_token) is OAuth2Token:
            self._oauth2_token = str(pickle.dumps(oauth2_token))
        elif oauth2_token is None:
            self._oauth2_token = ''
        else:
            raise TypeError('Expected type OAuth2Token or None')
    
    def revoke_oauth2_token(self):
        client = self.get_gdata_client()
        client.revoke_token()
        self.oauth2_token = None

