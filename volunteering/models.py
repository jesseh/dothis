import random

from django.db import models

OBSCURE_SLUG_LENGTH = 8
OBSCURE_SLUG_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Volunteer(models.Model):

    name = models.CharField(max_length=200)
    external_id = models.CharField(max_length=200, null=True, blank=True,
                                   unique=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)
    obscure_slug = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.name

    def generate_obscure_slug(self):
        length = OBSCURE_SLUG_LENGTH + 1
        while True:
            slug_chars = [random.choice(OBSCURE_SLUG_ALPHABET)
                          for i in xrange(length)]
            slug_chars[4] = '-'
            slug = "".join(slug_chars)
            if not Volunteer.objects.filter(obscure_slug=slug).exists():
                break
        return slug

    def save(self, *args, **kwargs):
        if self.obscure_slug is None or self.obscure_slug == '':
            self.obscure_slug = self.generate_obscure_slug()
        if self.external_id == '':
            self.external_id is None
        super(Volunteer, self).save(*args, **kwargs)

    def assignable_duty_names(self):
        return ", ".join(d.name for d in Duty.objects.unassigned())

    def assigned_duty_names(self):
        duty_names = (d.name for d in self.duty_set.all())
        return ", ".join(duty_names)


class DutyManager(models.Manager):
    def unassigned(self):
        return self.get_queryset().filter(assigned_to=None)


class Duty(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign)
    assigned_to = models.ForeignKey(Volunteer, null=True, blank=True)
    attributes = models.ManyToManyField(Attribute)

    objects = DutyManager()

    def __unicode__(self):
        return self.name
