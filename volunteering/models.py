import random

from django.db import models
from django.db.models import F, Count, Q
from django.core.urlresolvers import reverse
from django.utils.timezone import now as datetime_now
from django.template.defaultfilters import escape

from django_extensions.db.models import ActivatorModel, TimeStampedModel

SLUG_LENGTH = 8
SLUG_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'
TIME_FORMAT = "%H:%M"


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Campaign(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    events = models.ManyToManyField('Event', null=True, blank=True)
    locations = models.ManyToManyField('Location', null=True, blank=True)
    activities = models.ManyToManyField('Activity', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def deactivate(self):
        self.status = ActivatorModel.INACTIVE_STATUS
        self.deactivate_date = datetime_now()

    def duties(self):
        duties = Duty.objects.filter(
            Q(event__campaign=self)
            | Q(location__campaign=self)
            | Q(activity__campaign=self)).distinct()
        return duties

    def recipients(self, assigned=False, assignable=False):
        duties = self.duties
        assigned_q = Q(assignment__duty__in=duties)
        assignable_q = Q(attributes__activity__duty__in=duties)

        if assigned and assignable:
            q_def = assigned_q | assignable_q
        elif assigned:
            q_def = assigned_q
        elif assignable:
            q_def = assignable_q
        else:
            raise ValueError("At least assigned or assignable must be true.")

        return Volunteer.objects.filter(q_def).distinct()

    def recipient_count(self):
        return self.recipients(assignable=True, assigned=True).count()

    def recipient_names(self):
        recipients = self.recipients(assigned=True,
                                     assignable=True).order_by('first_name')
        names = ("%s - %s" % (v.name(), v.email_address) for v in recipients)
        if names:
            return "<ul><li>%s</li></ul>" % "</li><li>".join(names)
        else:
            return ""
    recipient_names.allow_tags = True
    recipient_names.short_description = "Recipients"


class Message(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Trigger(models.Model):
    ASSIGNED, ASSIGNABLE, ASSIGNED_AND_ASSIGNABLE = range(3)
    ASSIGNMENT_STATES = (
        (ASSIGNED, 'Assigned'),
        (ASSIGNABLE, 'Assignable'),
        (ASSIGNED_AND_ASSIGNABLE, 'Assigned and assignable'),
    )

    campaign = models.ForeignKey(Campaign, null=True, blank=True)
    message = models.ForeignKey(Message, null=True, blank=True)
    fixed_date = models.DateField(
        null=True, blank=True,
        help_text="Send the message on this specific day. If today "
                  "or earlier the message will go immediately")
    fixed_assignment_state = models.IntegerField(
        choices=ASSIGNMENT_STATES,
        default=ASSIGNED_AND_ASSIGNABLE)
    event_based_days_before = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Send the message this many days before the event.")
    event_based_assignment_state = models.IntegerField(
        choices=ASSIGNMENT_STATES,
        default=ASSIGNED_AND_ASSIGNABLE)
    assignment_based_days_after = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Send the message this many days after the role "
                  "was assigned to the volunteer (including them assigning "
                  "it themself). '0' will send the day they are assigned.")

    def __unicode__(self):
        return "%s: %s" % (self.campaign, self.message)


class Family(models.Model):
    external_id = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.external_id

    def surnames(self):
        surnames = self.volunteer_set.order_by('surname').distinct(
            ).values_list('surname', flat=True)
        return ", ".join(surnames)

    def names(self):
        names = [v.name() for v in self.volunteer_set.all()]
        return ", ".join(sorted(names))


class Volunteer(models.Model):
    title = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True, db_index=True)
    surname = models.CharField(max_length=200, db_index=True)
    dear_name = models.CharField(
        max_length=200, blank=True,
        help_text="Leave blank if same as first name")
    external_id = models.CharField(max_length=200, unique=True)
    family = models.ForeignKey(Family)
    email_address = models.EmailField(blank=True)
    home_phone = models.CharField(max_length=200, blank=True)
    mobile_phone = models.CharField(max_length=200, blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)
    slug = models.CharField(max_length=10, unique=True, blank=True)

    def __unicode__(self):
        return "%s %s (%s)" % (self.first_name, self.surname, self.external_id)

    def get_absolute_url(self):
        return reverse('volunteering:summary',
                       kwargs={'volunteer_slug': self.slug})

    def name(self):
        return "%s %s" % (self.first_name, self.surname)

    def initials(self):
        return '%s.%s.' % (self.first_name[0], self.surname[0])

    def family_link(self):
        return '<a href="%s">%s</a>' % (
            reverse("admin:volunteering_family_change",
                    args=(self.family_id,)),
            escape(self.family.external_id))

    family_link.allow_tags = True
    family_link.short_description = "Family"

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

    def attributes_list(self):
        return ", ".join(self.attributes.values_list('name', flat=True))


class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (("name", "date"))
        ordering = ['date']

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date)


class Activity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def attributes_list(self):
        return ", ".join(self.attributes.values_list('name', flat=True))


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class AssignableDutyManager(models.Manager):
    def assignable(self):
        return super(AssignableDutyManager, self). \
            get_queryset(). \
            annotate(num_assignments=Count('assignments')). \
            filter(num_assignments__lt=F('multiple')). \
            filter(multiple__gt=0)

    def assignable_to(self, volunteer):
        return self.assignable(). \
            filter(assignment__isnull=True). \
            filter(
                Q(activity__attributes__volunteer=volunteer) |
                Q(activity__attributes__isnull=True)
            ).exclude(assignment__volunteer=volunteer)


class Duty(models.Model):
    activity = models.ForeignKey(Activity, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    multiple = models.PositiveIntegerField(
        default=1,
        help_text="The number of volunteers needed for this duty.")
    assignments = models.ManyToManyField(Volunteer, through='Assignment')
    details = models.TextField(blank=True)
    coordinator_note = models.TextField(blank=True)

    objects = AssignableDutyManager()

    class Meta:
        unique_together = (("activity", "event", "location", "start_time",
                            "end_time"))
        verbose_name_plural = "Duties"

    def __unicode__(self):
        name = ""
        if self.activity:
            name += self.activity.name
        if self.event:
            name += " on " + self.event.name
        if self.location:
            name += " at " + self.location.name
        if self.times_string():
            name += " (%s)" % self.times_string()
        return name

    def times_string(self):
        if self.start_time and self.end_time:
            return "%s - %s" % (self.start_time.strftime(TIME_FORMAT),
                                self.end_time.strftime(TIME_FORMAT))
        elif self.start_time:
            return self.start_time
        else:
            return ''

    def unassigned_count(self):
        return self.multiple - self.assignment_set.count()


class Assignment(TimeStampedModel):
    volunteer = models.ForeignKey(Volunteer)
    duty = models.ForeignKey(Duty)

    class Meta:
        unique_together = (("volunteer", "duty"),)

    def __unicode__(self):
        return "%s -> %s" % (self.volunteer.name(), str(self.duty))

    def get_absolute_url(self):
        return reverse(
            'volunteering:assignment',
            kwargs={'volunteer_slug': self.volunteer.slug,
                    'duty_id': self.duty_id})
