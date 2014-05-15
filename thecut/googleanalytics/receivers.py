# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def clear_cache(sender, instance, **kwargs):

    if not kwargs.get('raw', False):
        from .models import Profile
        Profile.objects.clear_cache()
