from django.contrib.sites.models import Site
try:
  from django.db import models
except:
  print 'what?'


class AnalyticsWebProperty(models.Model):
    """A sites Google Analytics web property settings.
    
    Google Analytics profiles can be created at:
    http://www.google.com/analytics/
    
    """
    site = models.OneToOneField(Site, unique=True)
    web_property_id = models.CharField(max_length=25,
        help_text='Web Property ID is obtained when \
        <a href="http://www.google.com/analytics/" target="_new">\
        configuring the site profile in Google Analytics</a>.')
    
    is_enabled = models.BooleanField(default=False,
        help_text='Is Google Analytics tracking enabled on the website?')
    
    class Meta:
        ordering = ['site']
        verbose_name = 'web property'
        verbose_name_plural = 'web properties'
    
    def __unicode__(self):
        return self.site.name

