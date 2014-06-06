from django.db import models

from taggit.managers import TaggableManager


class Campaign(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Volunteer(models.Model):
    name = models.CharField(max_length=200)
    external_id = models.CharField(max_length=200, null=True, blank=True,
                                   unique=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.name

    def assignable_duty_names(self):
        return ", ".join(d.name for d in Duty.objects.unassigned())

    def assigned_duty_names(self):
        duty_names = (d.name for d in self.duty_set.all())
        return ", ".join(duty_names)

    def save(self, *args, **kwargs):
        if self.external_id == "":
            self.external_id = None
        super(Volunteer, self).save(*args, **kwargs)


class DutyManager(models.Manager):
    def unassigned(self):
        return self.get_queryset().filter(assigned_to=None)


class Duty(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign)
    assigned_to = models.ForeignKey(Volunteer, null=True, blank=True)

    objects = DutyManager()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.name
