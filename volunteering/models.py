import random

from django.db import models
from django.core.urlresolvers import reverse

SLUG_LENGTH = 8
SLUG_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


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

    def assignable_duty_names(self):
        return ", ".join(d.name for d in Duty.objects.unassigned())

    def assigned_duty_names(self):
        duty_names = (d.name for d in self.duty_set.all())
        return ", ".join(duty_names)

    def has_claimed(self, duty):
        return duty in self.duty_set.all()


class DutyManager(models.Manager):
    def unassigned(self):
        return self.get_queryset().filter(assigned_to=None)


class Duty(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    campaign = models.ForeignKey(Campaign)
    assigned_to = models.ForeignKey(Volunteer, null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)

    objects = DutyManager()

    def __unicode__(self):
        return self.name
