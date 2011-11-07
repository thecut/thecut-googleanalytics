# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db.models import Manager, ObjectDoesNotExist


ANALYTICS_CACHE = {}


class AnalyticsWebPropertyManager(Manager):
    def get_current(self):
        """
        Returns the ``AnalyticsWebProperty`` for the current site.
        
        The ``AnalyticsWebProperty`` object is cached the first time it's
        retrieved from the database.
        """
        site = Site.objects.get_current()
        analytics_web_property = ANALYTICS_CACHE.get(site.pk, None)
        if analytics_web_property is None:
            analytics_web_property = self.get(site=site)
            ANALYTICS_CACHE[site.pk] = analytics_web_property
        return analytics_web_property
    
    def clear_cache(self):
        """Clears the ``AnalyticsWebProperty`` object cache."""
        global ANALYTICS_CACHE
        ANALYTICS_CACHE = {}

