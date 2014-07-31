import random

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timezone import now as datetime_now

from django_extensions.db.models import ActivatorModel, TimeStampedModel

SLUG_LENGTH = 8
SLUG_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Campaign(ActivatorModel, TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    campaign = models.ManyToManyField('Event', through='CampaignEvent',
                                      null=True, blank=True)

    def __unicode__(self):
        return self.name

    def deactivate(self):
        self.status = ActivatorModel.INACTIVE_STATUS
        self.deactivate_date = datetime_now()


class Volunteer(models.Model):

    name = models.CharField(max_length=200)
    external_id = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)
    slug = models.CharField(max_length=10, unique=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('volunteering:summary',
                       kwargs={'volunteer_slug': self.slug})

    def generate_slug(self):
        length = SLUG_LENGTH + 1
        while True:
            slug_chars = [random.choice(SLUG_ALPHABET)
                          for i in xrange(length)]
            slug_chars[4] = '-'
            slug = "".join(slug_chars)
            if not Volunteer.objects.filter(slug=slug).exists():
                break
        return slug

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = self.generate_slug()
        if self.external_id == '':
            self.external_id is None
        super(Volunteer, self).save(*args, **kwargs)

    def has_claimed(self, duty):
        return Assignment.objects.filter(volunteer=self, duty=duty).exists()


class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (("name", "date"))

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date)


class Activity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_description = models.TextField(null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Duty(models.Model):
    activity = models.ForeignKey(Activity, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    multiple = models.IntegerField(
        default=1,
        help_text="The number of volunteers needed for this duty.")
    assignments = models.ManyToManyField(Volunteer, through='Assignment')

    class Meta:
        unique_together = (("activity", "event", "location"))

    def __unicode__(self):
        name = ""
        if self.activity:
            name += self.activity.name
        if self.event:
            name += " on " + self.event.name
        if self.location:
            name += " at " + self.location.name
        return name


class CampaignEvent(TimeStampedModel):
    campaign = models.ForeignKey(Campaign)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return "%s: %s" % (self.campaign, self.event)


class Assignment(TimeStampedModel):
    volunteer = models.ForeignKey(Volunteer)
    duty = models.ForeignKey(Duty)

    class Meta:
        unique_together = (("volunteer", "duty"),)

    def __unicode__(self):
        return "%s -> %s" % (self.volunteer.name, str(self.duty))

    def get_absolute_url(self):
        return reverse(
            'volunteering:assignment',
            kwargs={'volunteer_slug': self.volunteer.slug,
                    'duty_id': self.duty_id})
