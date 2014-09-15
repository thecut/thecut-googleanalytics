# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.utils.datastructures import SortedDict
from thecut.googleanalytics.models import Profile


class ProfileAdminForm(forms.ModelForm):

    class Meta(object):
        model = Profile
        fields = ['site', 'web_property_id', 'display_features', 'is_enabled']

    def __init__(self, *args, **kwargs):
        super(ProfileAdminForm, self).__init__(*args, **kwargs)

        if 'web_property_id' in self.fields:
            self.fields['web_property_id'].widget.attrs.update(
                {'placeholder': 'UA-xxxxxxxx-x'})


class GoogleAPIProfileAdminForm(ProfileAdminForm):

    class Meta(ProfileAdminForm.Meta):
        fields = ['site', 'profile_id', 'display_features', 'is_enabled']

    def __init__(self, *args, **kwargs):
        super(GoogleAPIProfileAdminForm, self).__init__(*args, **kwargs)
        self.fields['profile_id'].label = 'View (profile)'
        analytics_username = self.get_account_summaries()['username']
        self.fields['profile_id'].help_text = 'Google Analytics views ' \
            '(profiles) for {0}'.format(analytics_username)
        self.fields['profile_id'].required = True
        self.fields['profile_id'].widget = forms.Select(
            choices=self.get_profile_choices())

    def get_profiles_list(self):
        service = self.instance.get_analytics_google_api_client()
        request = service.management().profiles().list(
            webPropertyId='~all', accountId='~all',
            fields='items(id,name,webPropertyId),username')
        return request.execute()

    def get_account_summaries(self):
        # TODO: Pagination?
        if not hasattr(self, '_account_summaries'):
            service = self.instance.get_analytics_google_api_client()
            request = service.management().accountSummaries().list()
            self._account_summaries = request.execute()
        return self._account_summaries

    def get_profiles(self):
        if not hasattr(self, '_profiles'):
            self._profiles = SortedDict()
            for account in self.get_account_summaries()['items']:
                for web_property in account['webProperties']:
                    for profile in web_property['profiles']:
                        self._profiles.update({
                            profile['id']: {'profile': profile,
                                            'web_property': web_property,
                                            'account': account}})
        return self._profiles

    def get_profile_choices(self):
        choices = []
        for profile_id, data in self.get_profiles().items():
            label = ' | '.join([data['account']['name'],
                                data['web_property']['name'],
                                data['profile']['name']])
            choices += [(profile_id, label)]
        return choices

    def save(self, *args, **kwargs):
        profile = self.get_profiles()[self.cleaned_data['profile_id']]
        self.instance.web_property_id = profile['web_property']['id']
        return super(GoogleAPIProfileAdminForm, self).save(*args, **kwargs)
