# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Profile
from django.contrib import messages
from django.contrib.admin.options import csrf_protect_m
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.views import generic
from oauth2client.client import FlowExchangeError, OAuth2WebServerFlow
import base64
import pickle


class OAuth2RequestTokenView(generic.detail.SingleObjectMixin, generic.View):

    model = Profile
    scope = 'https://www.googleapis.com/auth/analytics'

    @csrf_protect_m
    @method_decorator(permission_required('googleanalytics.change_profile'))
    def dispatch(self, *args, **kwargs):
        return super(OAuth2RequestTokenView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.model.objects.clear_cache()
        self.object = self.get_object()
        flow = self.get_flow()
        self.request.session['oauth2_googleanalytics_profile'] = self.object.pk
        self.request.session['oauth2_flow'] = base64.b64encode(
            pickle.dumps(flow))
        self.request.session.modified = True
        return HttpResponseRedirect(flow.step1_get_authorize_url())

    def get_flow(self):
        return OAuth2WebServerFlow(
            client_id=settings.GOOGLE_API_CLIENT_ID,
            client_secret=settings.GOOGLE_API_CLIENT_SECRET,
            scope=self.get_scope(), redirect_uri=self.get_redirect_url(),
            user_agent=settings.USER_AGENT, access_type='offline')

    def get_scope(self):
        return self.scope

    def get_redirect_url(self):
        return self.request.build_absolute_uri('../callback')


class OAuth2CallbackView(generic.View):

    object = None

    def exchange_token(self, flow, code):
        try:
            credentials = flow.step2_exchange(code)
        except FlowExchangeError:
            # TODO: Error Handling
            raise
        else:
            self.object.oauth2_credentials = credentials
            Profile.objects.clear_cache()
            messages.success(self.request, 'Linked Google Analytics account.')

    @csrf_protect_m
    @method_decorator(permission_required('googleanalytics.change_profile'))
    def dispatch(self, *args, **kwargs):
        return super(OAuth2CallbackView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        profile_pk = self.request.session.pop('oauth2_googleanalytics_profile',
                                             None)
        try:
            self.object = Profile.objects.get(pk=profile_pk)
        except Profile.DoesNotExist:
            self.object = None

        pickled_flow = self.request.session.pop('oauth2_flow', None)
        code = self.request.GET.get('code', None)
        self.request.session.modified = True

        if None in [self.object, pickled_flow, code]:
            # TODO: Error handling
            return HttpResponseBadRequest()
        else:
            flow = pickle.loads(base64.b64decode(pickled_flow))
            self.exchange_token(flow, code)
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return '../{0}/'.format(self.object.pk)


class OAuth2RevokeTokenView(generic.edit.DeleteView):

    admin = None
    model = Profile
    template_name_suffix = '_confirm_revoke'

    def delete(self, *args, **kwargs):
        profile = self.get_object()
        profile.revoke_oauth2_credentials()
        profile.profile_id = ''
        profile.save()
        self.model.objects.clear_cache()
        messages.success(self.request, 'Unlinked Google Analytics account.')
        return HttpResponseRedirect(self.get_success_url())

    @csrf_protect_m
    @method_decorator(permission_required('googleanalytics.change_profile'))
    def dispatch(self, *args, **kwargs):
        return super(OAuth2RevokeTokenView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(OAuth2RevokeTokenView, self).get_context_data(
            *args, **kwargs)
        opts = self.admin.model._meta
        defaults = {
            'current_app': self.admin.admin_site.name,
            'opts': opts,
            'app_label': opts.app_label,
            'title': 'Unlink {0}'.format(
                force_unicode(opts.verbose_name_plural)),
            'root_path': reverse(
                '{0}:index'.format(self.admin.admin_site.name)),
            'base_template': '{0}/change_form.html'.format(
                self.admin.admin_site.name)}
        for key, value in defaults.items():
            context_data.setdefault(key, value)
        return context_data

    def get_object(self, *args, **kwargs):
        obj = super(OAuth2RevokeTokenView, self).get_object(*args, **kwargs)
        if not obj.use_google_api():
            raise Http404()
        return obj

    def get_template_names(self):
        current_app = self.admin.admin_site.name
        app_label = self.admin.model._meta.app_label
        model_name = self.admin.model._meta.object_name.lower()

        return [
            '{0}/{1}/{2}/revoke_confirmation.html'.format(
                current_app, app_label, model_name),
            'admin/{0}/{1}/revoke_confirmation.html'.format(
                app_label, model_name)
        ]

    def get_success_url(self):
        return '../../'
