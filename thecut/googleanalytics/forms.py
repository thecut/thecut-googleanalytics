# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut.googleanalytics.models import Profile


class ProfileAdminForm(forms.ModelForm):

    class Meta(object):
        model = Profile
        fields = ('site', 'web_property_id', 'display_advertiser_support',
                  'is_enabled')


class GoogleAPIProfileAdminForm(forms.ModelForm):

    class Meta(object):
        model = Profile
        fields = ('site', 'profile_id', 'display_advertiser_support',
                  'is_enabled')

    def __init__(self, *args, **kwargs):
        super(GoogleAPIProfileAdminForm, self).__init__(*args, **kwargs)
        self.profiles = {}

        api_response = self.get_profiles_list()

        for profile in api_response.get('items', []):
            self.profiles.update({profile['id']: profile})

        self.fields['profile_id'].label = 'Profile'
        self.fields['profile_id'].help_text = 'Google Analytics profiles ' \
            'for {0}'.format(api_response['username'])
        self.fields['profile_id'].required = True
        self.fields['profile_id'].widget = forms.Select(
            choices=self.get_profile_choices())

    def get_profiles_list(self):
        service = self.instance.get_analytics_google_api_client()
        request = service.management().profiles().list(
            webPropertyId='~all', accountId='~all',
            fields='items(id,name,webPropertyId),username')
        return request.execute()

    def get_profile_choices(self):
        return [(profile['id'], profile['name']) for profile in
                self.profiles.values()]

    def save(self, *args, **kwargs):
        profile = self.profiles[self.cleaned_data['profile_id']]
        self.instance.web_property_id = profile['webPropertyId']
        return super(GoogleAPIProfileAdminForm, self).save(*args, **kwargs)
