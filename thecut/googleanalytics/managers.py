# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db.models import Manager, ObjectDoesNotExist


ANALYTICS_CACHE = {}


class ProfileManager(Manager):
    def get_current(self):
        """
        Returns the ``Profile`` for the current site.
        
        The ``Profile`` object is cached the first time it's
        retrieved from the database.
        """
        site = Site.objects.get_current()
        profile = ANALYTICS_CACHE.get(site.pk, None)
        if profile is None:
            profile = self.get(site=site)
            ANALYTICS_CACHE[site.pk] = profile
        return profile
    
    def clear_cache(self):
        """Clears the ``Profile`` object cache."""
        global ANALYTICS_CACHE
        ANALYTICS_CACHE = {}

