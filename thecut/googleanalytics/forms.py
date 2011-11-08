# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut.googleanalytics.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta(object):
        model = Profile
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.use_gdata():
            self.fields['web_property_id'].label = 'Web property'
            self.fields['web_property_id'].help_text = None
            self.fields['web_property_id'].widget = forms.Select(
                choices=self.get_web_property_choices())
    
    def get_web_property_choices(self):
        choices = []
        if self.instance.use_gdata():
            from gdata.analytics.client import ProfileQuery
            client = self.instance.get_gdata_client()
            feed = client.GetManagementFeed(ProfileQuery())
            for entry in feed.entry:
                web_property_id = entry.GetProperty('ga:webPropertyId').value
                profile_name = entry.GetProperty('ga:profileName').value
                choices += [(web_property_id, profile_name)]
        return choices

