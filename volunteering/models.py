import logging
import random
from datetime import date

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Count, Q, Sum
from django.template import Context, Template
from django.template.defaultfilters import escape
from django.utils.timezone import now as datetime_now

from django_extensions.db.models import ActivatorModel, TimeStampedModel

from djrill.exceptions import MandrillAPIError

SLUG_LENGTH = 8
SLUG_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'
TIME_FORMAT = "%H:%M"

logger = logging.getLogger(__name__)


class Attribute(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Campaign(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    events = models.ManyToManyField('Event', null=True, blank=True)
    locations = models.ManyToManyField('Location', null=True, blank=True)
    activities = models.ManyToManyField('Activity', null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def deactivate(self):
        self.status = ActivatorModel.INACTIVE_STATUS
        self.deactivate_date = datetime_now()

    def related_duties_q(self):
        q_objects = []

        if self.events.exists():
            q_objects.append(Q(event__campaign=self))
        if self.locations.exists():
            q_objects.append(Q(location__campaign=self))
        if self.activities.exists():
            q_objects.append(Q(activity__campaign=self))
        return Q(*q_objects)

    def duties(self):
        return Duty.objects.filter(self.related_duties_q()).distinct()

    def volunteers_needed(self):
        return self.duties().aggregate(Sum('multiple'))['multiple__sum'] or 0

    def volunteers_assigned(self):
        return Assignment.objects.filter(duty__in=self.duties()).count()

    def percent_assigned(self):
        total = self.volunteers_needed()
        assigned = self.volunteers_assigned()
        percent = 0
        if total > 0:
            percent = 100 * assigned / total
        return "%s%%" % percent

    def recipients(self, assigned=False, assignable=False, unassigned=False):
        duties = self.duties
        assigned_q = Q(assignment__duty__in=duties)
        assignable_q = Q(attributes__activity__duty__in=duties)

        if unassigned and (assigned or assignable):
            raise ValueError("At least assigned or assignable must be true.")
        elif unassigned:
            q_def = assignable_q & ~assigned_q
        elif assigned and assignable:
            q_def = assigned_q | assignable_q
        elif assigned:
            q_def = assigned_q
        elif assignable:
            q_def = assignable_q
        else:
            raise ValueError("At least assigned, assignable, or unassigned "
                             "must be true.")

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
    body_is_html = models.BooleanField(default=False)

    def _render(self, source, context_dict):
        t = Template(source)
        c = Context(context_dict)
        return t.render(c)

    def rendered_body(self, context_dict):
        return self._render(self.body, context_dict)

    def rendered_subject(self, context_dict):
        return self._render(self.subject, context_dict)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class TriggerBase(models.Model):
    ASSIGNED, ASSIGNABLE, ASSIGNED_AND_ASSIGNABLE, UNASSIGNED = range(4)
    ASSIGNMENT_STATES = (
        (ASSIGNED, 'With an assigned duty'),
        (ASSIGNABLE, 'Assignable to a duty'),
        (ASSIGNED_AND_ASSIGNABLE, 'All recipients'),
        (UNASSIGNED, 'No assigned duties'),
    )

    campaign = models.ForeignKey(Campaign, null=True, blank=True)
    message = models.ForeignKey(Message, null=True, blank=True)

    class Meta:
        ordering = ['campaign']
        abstract = True

    def __unicode__(self):
        return "%s: %s" % (self.campaign, self.message)

    def recipients(self):
        raise NotImplementedError


class TriggerByAssignment(TriggerBase):
    days_after = models.PositiveIntegerField(
        help_text="Send the message this many days after the role "
                  "was assigned to the volunteer (including them assigning "
                  "it themself). '0' will send the day they are assigned.")


class TriggerByEvent(TriggerBase):
    days_before = models.PositiveIntegerField(
        help_text="Send the message this many days before the event.")
    assignment_state = models.IntegerField(
        choices=TriggerBase.ASSIGNMENT_STATES,
        default=TriggerBase.ASSIGNED_AND_ASSIGNABLE)


class TriggerQuerySet(models.QuerySet):
    def triggered(self, trigger_date):
        q_fixed_date = Q(fixed_date=trigger_date)

        q_get_assigned = Q(assignment_state=TriggerBase.ASSIGNED)
        q_get_assignable = Q(assignment_state=TriggerBase.ASSIGNABLE)
        q_get_assigned_and_assignable = Q(
            assignment_state=TriggerBase.ASSIGNED_AND_ASSIGNABLE)
        q_get_unassigned = Q(assignment_state=TriggerBase.UNASSIGNED)

        q_has_assigned = Q(campaign__events__duty__assignments__isnull=False)

        q_assigned = Q(q_get_assigned & q_has_assigned)
        q_assignable = Q(q_get_assignable)
        q_assigned_and_assignable = Q(q_get_assigned_and_assignable)
        q_unassigned = Q(q_get_unassigned)

        return self. \
            filter(q_fixed_date). \
            filter(q_assigned | q_assignable |
                   q_assigned_and_assignable | q_unassigned)


class TriggerByDate(TriggerBase):

    fixed_date = models.DateField(
        null=True, blank=True, db_index=True,
        help_text="Send the message on this specific day. If today "
                  "or earlier the message will go immediately")
    assignment_state = models.IntegerField(
        choices=TriggerBase.ASSIGNMENT_STATES,
        default=TriggerBase.ASSIGNED_AND_ASSIGNABLE)

    objects = TriggerQuerySet.as_manager()

    def assigned(self):
        return self.assignment_state == TriggerBase.ASSIGNED or \
            self.assignment_state == TriggerBase.ASSIGNED_AND_ASSIGNABLE

    def assignable(self):
        return self.assignment_state == TriggerBase.ASSIGNABLE or \
            self.assignment_state == TriggerBase.ASSIGNED_AND_ASSIGNABLE

    def unassigned(self):
        return self.assignment_state == TriggerBase.UNASSIGNED

    def recipients(self):
            return self.campaign.recipients(assigned=self.assigned(),
                                            assignable=self.assignable(),
                                            unassigned=self.unassigned())


class Family(models.Model):
    REGENT_SUITE, SHUL = (1, 2)
    SERVICE_LOCATIONS = (
        (REGENT_SUITE, 'Regent Suite'),
        (SHUL, 'Shul'),
    )
    external_id = models.CharField(max_length=200, unique=True)
    hh_location_2014 = models.IntegerField(choices=SERVICE_LOCATIONS,
                                           null=True, blank=True)

    class Meta:
        ordering = ['external_id']

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
    last_summary_view = models.DateTimeField(null=True)
    note = models.TextField(blank=True)
    temporary_change = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['surname']

    def __unicode__(self):
        return "%s, %s (%s)" % (self.surname, self.first_name,
                                self.external_id)

    def get_absolute_url(self):
        return reverse('volunteering:summary',
                       kwargs={'volunteer_slug': self.slug})

    def name(self):
        return "%s %s" % (self.first_name, self.surname)

    def formal_name(self):
        if self.title:
            return "%s %s" % (self.title, self.surname)
        else:
            return self.surname

    def to_name(self):
        return self.dear_name or self.first_name or self.formal_name()

    def initials(self):
        return '%s.%s.' % (self.first_name[0], self.surname[0])

    def summary_url(self):
        return self.get_absolute_url()

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
            filter(
                Q(activity__attributes__volunteer=volunteer) |
                Q(activity__attributes__isnull=True)
            ).exclude(assignment__volunteer=volunteer)


class Duty(models.Model):
    activity = models.ForeignKey(Activity, null=True, blank=True,
                                 db_index=True)
    event = models.ForeignKey(Event, null=True, blank=True, db_index=True)
    location = models.ForeignKey(Location, null=True, blank=True,
                                 db_index=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    multiple = models.PositiveIntegerField(
        default=1,
        help_text="The number of volunteers needed for this duty.")
    assignments = models.ManyToManyField(Volunteer, through='Assignment',
                                         db_index=True)
    details = models.TextField(blank=True)
    coordinator_note = models.TextField(blank=True)

    objects = AssignableDutyManager()

    class Meta:
        unique_together = (("activity", "event", "location", "start_time",
                            "end_time"))
        verbose_name_plural = "Duties"
        ordering = ['event', 'start_time', 'activity', 'location']

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
    volunteer = models.ForeignKey(Volunteer, db_index=True)
    duty = models.ForeignKey(Duty, db_index=True)
    assigned_location = models.ForeignKey(Location, null=True, blank=True,
                                          db_index=True)

    class Meta:
        unique_together = (("volunteer", "duty"),)

    def __unicode__(self):
        return "%s -> %s" % (self.volunteer.name(), str(self.duty))

    def get_absolute_url(self):
        return reverse(
            'volunteering:assignment',
            kwargs={'volunteer_slug': self.volunteer.slug,
                    'duty_id': self.duty_id})

    def hh_service_location(self):
        return self.volunteer.family.get_hh_location_2014_display()

    def duty_link(self):
        return '<a href="%s">%s</a>' % (
            reverse("admin:volunteering_duty_change", args=(self.duty_id,)),
            escape(str(self.duty)))
    duty_link.allow_tags = True
    duty_link.short_description = "Duty"


class Sendable(TimeStampedModel):
    send_date = models.DateField(db_index=True)
    volunteer = models.ForeignKey(Volunteer, db_index=True)
    assignment = models.ForeignKey(Assignment, null=True, blank=True)
    sent_date = models.DateField(null=True, blank=True, db_index=True)
    send_failed = models.BooleanField(default=False, db_index=True)
    trigger_type = models.ForeignKey(ContentType)
    trigger_id = models.PositiveIntegerField()
    trigger = GenericForeignKey('trigger_type', 'trigger_id')

    class Meta:
        unique_together = (("send_date", "trigger_type", "trigger_id",
                            "volunteer", "assignment"),)

    def __unicode__(self):
        return "%s -> %s: %s" % (self.volunteer, self.trigger, self.send_date)

    def trigger_detail(self):
        return str(self.trigger)

    @classmethod
    def create_or_ignore(cls, trigger, volunteer, assignment, fixed_date):
        trigger_content_type = ContentType.objects.get_for_model(trigger)

        # create a sendable undless it already exists.
        s, created = Sendable.objects.get_or_create(
            trigger_id=trigger.id, trigger_type=trigger_content_type,
            volunteer=volunteer, assignment=None,
            send_date=fixed_date)

        # and note if it was created.
        if created:
            logger.info("Collected '%s'" % s)
        return created

    @classmethod
    def collect_from_fixed_triggers(cls, fixed_date):
        new_sendables_count = 0

        # Get all the triggers for the day
        for t in TriggerByDate.objects.triggered(fixed_date):
            print("Collecting %s" % t)

            # What duties are related to the campaign of this trigger (cache
            # this)?
            # REMOVE duties = t.campaign.duties()
            campaign_duties_q = t.campaign.related_duties_q()

            # Loop through the recipients
            for volunteer in t.recipients():
                print("  Collecting %s" % volunteer)

                # if assignability does not matter or if the volunteer can be
                # assigned to the duty
                if (not t.assignable()) or \
                        Duty.objects.assignable_to(volunteer). \
                        filter(campaign_duties_q).exists():
                    created = Sendable.create_or_ignore(t, volunteer, None,
                                                        fixed_date)
                    if created:
                        new_sendables_count += 1
        return new_sendables_count

    @classmethod
    def send_unsent(self):
        sent_count = 0
        for unsent in Sendable.objects.filter(
                sent_date__isnull=True).filter(send_failed=False):
            message = unsent.trigger.message
            context_dict = {'volunteer': unsent.volunteer,
                            'assignment': unsent.assignment}

            body = message.rendered_body(context_dict)

            email_params = {
                'subject': message.rendered_subject(context_dict),
                'to': [unsent.volunteer.email_address],
                'from_email': settings.FROM_ADDRESS,
            }

            if message.body_is_html:
                email = EmailMultiAlternatives(**email_params)
                email.attach_alternative(body, "text/html")
                email.auto_text = True
            else:
                email = EmailMessage(**email_params)
                email.body = body
                email.auto_html = True

            name_tag = ("name - %s" % message.name)[:50]
            trigger_tag = ("trigger - %s" % unsent.trigger.id)[:50]
            email.tags = [name_tag, trigger_tag]
            logger.info("Sending %s" % email_params)
            print("Sending %s" % email_params)
            try:
                email.send(fail_silently=False)
                unsent.sent_date = date.today()
                sent_count += 1
            except MandrillAPIError:
                print("FAILED %s" % email_params)
                unsent.send_failed = True
            unsent.save()
        return sent_count
