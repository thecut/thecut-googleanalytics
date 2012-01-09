# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


GDATA_CLIENT_ID = getattr(settings, 'GOOGLEANALYTICS_GDATA_CLIENT_ID', None)
GDATA_CLIENT_SECRET = getattr(settings, 'GOOGLEANALYTICS_GDATA_CLIENT_SECRET',
    None)

USE_GDATA = GDATA_CLIENT_ID is not None and GDATA_CLIENT_SECRET is not None

USER_AGENT = getattr(settings, 'GOOGLEANALYTICS_USER_AGENT',
    'thecut.googleanalytics/0.04 (The Cut; +http://www.thecut.net.au/')

