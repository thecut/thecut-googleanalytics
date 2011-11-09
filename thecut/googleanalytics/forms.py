# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut.googleanalytics.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta(object):
        model = Profile
        exclude = ['profile_id']


class GDataProfileForm(forms.ModelForm):
    class Meta(object):
        model = Profile
        exclude = ['web_property_id']
    
    def __init__(self, *args, **kwargs):
        super(GDataProfileForm, self).__init__(*args, **kwargs)
        if self.instance.use_gdata():
            self.fields['profile_id'].label = 'Profile'
            self.fields['profile_id'].required = True
            self.fields['profile_id'].widget = forms.Select(
                choices=self.get_profile_choices())
    
    def get_profile_feed(self):
        if self.instance.use_gdata():
            from gdata.analytics.client import ProfileQuery
            client = self.instance.get_gdata_client()
            return client.GetManagementFeed(ProfileQuery())
    
    def get_profile_choices(self):
        choices = []
        if self.instance.use_gdata():
            for entry in self.get_profile_feed().entry:
                profile_id = entry.GetProperty('ga:profileId').value
                profile_name = entry.GetProperty('ga:profileName').value
                choices += [(profile_id, profile_name)]
        return choices
    
    def save(self, *args, **kwargs):
        return super(GDataProfileForm, self).save(*args, **kwargs)

