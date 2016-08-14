from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as __

import re, datetime
from pytz import timezone
from django.core.validators import RegexValidator
from event.helpers import get_profile_pic_filename, get_image_filename

class Item(models.Model):
    is_visible = models.BooleanField(default=True)
    html_safe = models.BooleanField(default=False,
        verbose_name='HTML Safe?')

    rank = models.IntegerField(
        default=999, 
        help_text=_('For internal use. '
            'Determines the order in which this item or section appears on the website.')
        ) 

    # content
    title = models.CharField(max_length=100, default='Title')
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ('rank',)

class Section(Item):

    show_title = models.BooleanField(default=True,
        verbose_name='Show section title')
    page = models.ForeignKey('Page')
    template = models.CharField(max_length=50, default='section.html')

    # navigation
    show_in_nav = models.BooleanField(default=True,
        verbose_name='Show in navigation')
    nav_title = models.CharField(max_length=50, blank=True,
        help_text='The text appearing in the navbar',
        verbose_name='Navigation Title')

    class Meta:
        abstract = True
        ordering = ('rank',)

    def __unicode__(self):
        return self.title

class Cover(Section):
    SECTION_TYPE = 'cover'
    venue_short_name = models.CharField(max_length=200, blank=True,
        help_text="To display on the event cover")
    show_city = models.BooleanField(default=True)
    # section_ptr = models.IntegerField('Section', null=True, primary_key=False)

class About(Section):
    SECTION_TYPE = 'about'
    show_button = models.BooleanField(default=False)
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.URLField(max_length=100, blank=True)

class PerksSection(Section):
    SECTION_TYPE='perks'

class PerkItem(Item):
    section = models.ForeignKey('PerksSection', related_name='perks')
    fa_icon = models.CharField(max_length=20, blank=True,
        help_text='Icon code from http://fontawesome.io/icons/ (example: fa-coffee up will display the following icon http://fontawesome.io/icon/coffee/) ')
    image_icon = models.ImageField(null=True,
        help_text='Not advised. Image will be resized to 60x60 pixels', blank=True)

class SocialMediaSection(Section):
    SECTION_TYPE = 'social-media'
    hashtag = models.CharField(blank=True, max_length=20)

    show_tweet_link = models.BooleanField(default=False)
    tweet_link = models.TextField(blank=True, max_length=1000)

    show_facebook_link = models.BooleanField(default=False)
    facebook_link = models.TextField(blank=True, max_length=2000)
    facebook_text = models.TextField(blank=True, max_length=2000)
    facebook_name = models.TextField(blank=True, max_length=200)
    facebook_picture = models.TextField(blank=True, max_length=500)

class TalksSection(Section):
    SECTION_TYPE='talks'

class TalkItem(Item):
    section = models.ForeignKey('TalksSection',
        related_name='talks')
    speaker = models.ForeignKey('Person')

    def __unicode__(self):
        return '%s [%s]' % (self.title, self.section.title)

class WorkshopsSection(Section):
    SECTION_TYPE = 'workshops'

class WorkshopItem(Item):
    section = models.ForeignKey('WorkshopsSection',
        related_name='workshops')
    moderators = models.ManyToManyField('Person', blank=True)
    location = models.ForeignKey('Place', blank=True)
    time = models.DateTimeField(blank=True)
    duration = models.IntegerField(default=60, 
        help_text='In minutes.', blank=True)

    # IMAGE_FOLDER = 'workshops'
    # showcase_image = models.ImageField(
    #     upload_to=get_image_filename,
    #     help_text="Please make sure it's a transparent image (png).",
    #     blank=True)

    # @property
    # def all_moderators(self):
    #     return self.moderators.all()

    # @property
    # def human_readable_time_slot(self):
    #     start_time = self.time
    #     end_time = self.time + datetime.timedelta(0,self.duration*60)
    #     # convert times to local timezone
    #     eastern = timezone('US/Eastern')
    #     start_time = start_time.astimezone(eastern)        
    #     end_time = end_time.astimezone(eastern)        

    #     readable_time = '%s %s' % (
    #         datetime.datetime.strftime(start_time, '%A %I:%M%p - '),
    #         datetime.datetime.strftime(end_time, '%I:%M%p'),
    #     )
    #     return readable_time

    class Meta:
        ordering = ('time',)

    def __unicode__(self):
        return self.title

class FAQSection(Section):
    SECTION_TYPE = 'faq'

class FAQItem(models.Model):
    section = models.ForeignKey('FAQSection',
        related_name='questions')
    question = models.CharField(max_length=200)
    answer = models.TextField(blank='')

class VenueSection(Section):
    SECTION_TYPE = 'venue'
    venue = models.ForeignKey('Place', blank=True)

class TeamSection(Section):
    SECTION_TYPE = 'team'
    team_members = models.ManyToManyField('Person')

class SponsorsSection(Section):
    SECTION_TYPE='sponsors'
    sponsors = models.ManyToManyField('Sponsor')

class Sponsor(models.Model):
    company = models.ForeignKey('Company')
    CATEGORIES = (
        ('ST', _('Local Standard')),
        ('PR', _('Local Premium')),
        ('CM', _('Community')),
        ('PA', _('Partner')),
        ('GS', _('Global Standard')),
        ('GH', _('Global Premium')),
    )
    category = models.CharField(max_length=2, 
        choices=CATEGORIES, 
        default=CATEGORIES[0][0],
        )

    def get_verbose_category(self):
        return dict(CATEGORIES)[self.category]

    def __unicode__(self):
        return self.name

class PartnersSection(Section):
    SECTION_TYPE='partners'
    partners = models.ManyToManyField('Sponsor')


class ContactSection(Section):
    SECTION_TYPE = 'contact'
    contact_methods = models.ManyToManyField('SocialMediaAccount')

SECTION_CLASSES = (
    Cover,
    About,
    PerksSection,
    SocialMediaSection,
    TalksSection,
    WorkshopsSection,
    FAQSection,
    VenueSection,
    TeamSection,
    SponsorsSection,
    PartnersSection,
    ContactSection,
    )

class Page(models.Model):
    event = models.ForeignKey('Event', 
        related_name='pages')
    title = models.CharField(max_length=20)

    def get_sections(self):
        section_objs = []
        for section_class in SECTION_CLASSES:
            section_objs.extend(section_class.objects.filter(page=self).all())
        return section_objs

    def __unicode__(self):
        return self.title