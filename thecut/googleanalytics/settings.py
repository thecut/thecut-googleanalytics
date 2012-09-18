# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


# GData settings are deprecated
GDATA_CLIENT_ID = getattr(settings, 'GOOGLEANALYTICS_GDATA_CLIENT_ID', None)
GDATA_CLIENT_SECRET = getattr(settings, 'GOOGLEANALYTICS_GDATA_CLIENT_SECRET',
    None)
USE_GDATA = None not in [GDATA_CLIENT_ID, GDATA_CLIENT_SECRET]


GOOGLE_API_CLIENT_ID = getattr(settings,
    'GOOGLEANALYTICS_GOOGLE_API_CLIENT_ID', GDATA_CLIENT_ID)
GOOGLE_API_CLIENT_SECRET = getattr(settings,
    'GOOGLEANALYTICS_GOOGLE_API_CLIENT_SECRET', GDATA_CLIENT_SECRET)
USE_GOOGLE_API = None not in [GOOGLE_API_CLIENT_ID, GOOGLE_API_CLIENT_SECRET]


USER_AGENT = getattr(settings, 'GOOGLEANALYTICS_USER_AGENT',
    'thecut.googleanalytics/0.04.3 (The Cut; +http://www.thecut.net.au/)')

