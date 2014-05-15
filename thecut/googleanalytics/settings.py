# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


GOOGLE_API_CLIENT_ID = getattr(
    settings, 'GOOGLEANALYTICS_GOOGLE_API_CLIENT_ID', None)

GOOGLE_API_CLIENT_SECRET = getattr(
    settings, 'GOOGLEANALYTICS_GOOGLE_API_CLIENT_SECRET', None)

USE_GOOGLE_API = None not in [GOOGLE_API_CLIENT_ID, GOOGLE_API_CLIENT_SECRET]


USER_AGENT = getattr(settings, 'GOOGLEANALYTICS_USER_AGENT',
                     'thecut.googleanalytics/0.04.8 '
                     '(The Cut; +http://www.thecut.net.au/)')
