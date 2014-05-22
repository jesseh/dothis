from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Duty(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign)

    def __unicode__(self):
        return self.name


class Volunteer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
