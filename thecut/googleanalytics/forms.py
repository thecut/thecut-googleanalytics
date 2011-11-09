# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut.googleanalytics.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta(object):
        model = Profile
        exclude = ['profile_id']


class GDataProfileForm(forms.ModelForm):
    feed = None
    
    class Meta(object):
        model = Profile
        exclude = ['web_property_id']
    
    def __init__(self, *args, **kwargs):
        super(GDataProfileForm, self).__init__(*args, **kwargs)
        if self.instance.use_gdata():
            self.feed = self.get_profile_feed()
            self.fields['profile_id'].label = 'Profile'
            self.fields['profile_id'].required = True
            self.fields['profile_id'].widget = forms.Select(
                choices=self.get_profile_choices())
    
    def get_profile_feed(self):
        from gdata.analytics.client import ProfileQuery
        client = self.instance.get_gdata_client()
        return client.GetManagementFeed(ProfileQuery())
    
    def get_profile_choices(self):
        choices = []
        if self.instance.use_gdata() and self.feed is not None:
            for entry in self.feed.entry:
                profile_id = entry.GetProperty('ga:profileId').value
                profile_name = entry.GetProperty('ga:profileName').value
                choices += [(profile_id, profile_name)]
        return choices
    
    def get_web_property_for_profile(self, profile_id):
        for entry in self.feed.entry:
            if profile_id == entry.GetProperty('ga:profileId').value:
                return entry.GetProperty('ga:webPropertyId').value
    
    def save(self, *args, **kwargs):
        if self.instance.use_gdata() and self.feed is not None:
            self.instance.web_property_id = self.get_web_property_for_profile(
                self.cleaned_data['profile_id'])
        return super(GDataProfileForm, self).save(*args, **kwargs)

