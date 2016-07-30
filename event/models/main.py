from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as __

import re, datetime
from pytz import timezone
from django.core.validators import RegexValidator

class Event(models.Model):
    is_active = models.BooleanField(default=False)

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=100, blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.ForeignKey('Place')

    small_text_logo = models.ImageField(blank=True, 
        upload_to='event_text_logo',
        help_text="The logo appearing in the navbar")


    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

    social_media = models.ManyToManyField('SocialMediaAccount', blank=True)

    def __unicode__(self):
        return self.title
