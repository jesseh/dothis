from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Volunteer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def assignable_duties(self):
        duty_names = (d.name for d in Duty.unassigned_objects.all())
        return ", ".join(duty_names)


class UnassignedDutyManager(models.Manager):
    def get_queryset(self):
        return super(UnassignedDutyManager,
                     self).get_queryset().filter(assigned_to=None)


class Duty(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign)
    assigned_to = models.ForeignKey(Volunteer, null=True, blank=True)

    objects = models.Manager()
    unassigned_objects = UnassignedDutyManager()

    def __unicode__(self):
        return self.name
