from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as __

import re, datetime
from pytz import timezone
from django.core.validators import RegexValidator
from event.helpers import get_profile_pic_filename, get_image_filename

class SocialMediaAccount(models.Model):
	username = models.CharField(max_length=30)
	url = models.URLField(max_length=100, blank=True)

	ACCOUNT_TYPE_CHOICES = (
		('em', 'email'),
		('wb', 'website'),
		('tw', 'twitter'),
		('fb', 'facebook'),
		('gh', 'github'),
		('ln', 'linkedin')
		)

	account_types = models.CharField(max_length=2,
		choices = ACCOUNT_TYPE_CHOICES)

class PrizePerk(models.Model):
    rank = models.IntegerField(
        default=999, 
        help_text=_('For internal use. '
            'Determines the order in which this perk appears on the website.')
        )    
    description = models.TextField(
        help_text='This is HTML safe so you can use <a></a> tags for links, etc.')

    class Meta:
        ordering = ('rank',)

    def __unicode__(self):
        return '%i: %s' % (self.rank, self.description)

class Prize(models.Model):
    rank = models.IntegerField(
        default=999, 
        help_text=_('For internal use. '
            'Determines the order in which this perk appears on the website.')
        ) 
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=300,
        help_text='What to do to get this prize?', blank=True)
    perks = models.ManyToManyField('PrizePerk', blank=True)
    sponsor = models.ForeignKey('Sponsor', blank=True, null=True)
    image = models.ImageField(
        upload_to=get_image_filename,
        blank=True)
    fa_class = models.CharField(max_length=20, help_text='font-awesome class',
        default='star-o')

    class Meta:
        ordering = ('rank', 'title',)

    @property
    def all_perks(self):
        return self.perks.all()

    def __unicode__(self):
        return '%i: %s' % (self.rank, self.title)

class Company(models.Model):
    name = models.CharField(max_length=100)
    IMAGE_FOLDER = 'companies'
    image = models.ImageField(
        upload_to=get_image_filename,
        help_text="Please make sure it's a transparent image (png).")
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

class Person(models.Model):
    CATEGORIES = (
        ('O', _('Other')),
        ('J', _('Judge')),
        ('M', _('Mentor')),
    )

    alpha = RegexValidator(regex=re.compile(r'^[\w\s]*$', flags=re.UNICODE), message=_('Only letters are allowed.'))
    numeric = RegexValidator(regex=re.compile(r'^[\d]*$', flags=re.UNICODE), message=_('Only numbers are allowed.'))

    category = models.CharField(max_length=20, 
        choices=CATEGORIES, 
        default=CATEGORIES[0][0],
        )

    first_name = models.CharField(max_length=30, validators=[alpha])
    last_name = models.CharField(max_length=30, validators=[alpha])

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        # Translators: Gender information
        ('N', _('Other / I prefer not to disclose')),
    )
    gender = models.CharField(max_length=20, 
        choices=GENDER_CHOICES, 
        # default=GENDER_CHOICES[0][0],
        verbose_name=_('gender')
        )

    profile_pic = models.ImageField(blank=True, 
        upload_to=get_profile_pic_filename,
        help_text="Please make sure it's a square picture.")

    telephone = models.CharField(max_length=10, blank=True, validators=[numeric])

    company = models.CharField(max_length=100, blank=True)
    company_link = models.URLField(max_length=100, blank=True)

    rank = models.IntegerField(
        default=999, 
        help_text=_('For internal use. '
            'Determines the order in which this person appears on the website.')
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=100, 
        help_text="Appears under the person's name", blank=True)
    biography = models.TextField(blank=True)

    # social icons
    email = models.EmailField(blank=True)
    website = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)

    def full_name(self):
        return '%s %s' % (self.first_name.encode('utf-8'), 
            self.last_name.encode('utf-8'))
    full_name.admin_order_field = 'last_name'

    def has_twitter(self):
        return bool(self.twitter)

    def has_linkedin(self):
        return bool(self.linkedin)

    def has_website(self):
        return bool(self.website)

    def has_email(self):
        return bool(self.email)

    def has_facebook(self):
        return bool(self.facebook)

    def has_github(self):
        return bool(self.github)

    def has_telephone(self):
        return bool(self.telephone)

    class Meta:
        ordering = ('category', 'rank', 'last_name', 'updated_at', )

    def __unicode__(self):
        return self.full_name()

class Place(models.Model):
    address = models.ForeignKey('Address', null=True)
    short_display_name = models.CharField(max_length=100)

    website = models.URLField(max_length=200, blank=True)
    
    latitude = models.IntegerField(default=0,
        help_text="For Google Maps")
    longitude = models.IntegerField(default=0,
        help_text="For Google Maps")

    def __unicode__(self):
        return short_display_name

class Address(models.Model):
    num = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=6)

    def __unicode__(self):
        return '%i %s, %s, %s' % (self.num, self.street, self.city, self.province) 