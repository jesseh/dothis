import logging
import random
from datetime import date, timedelta, datetime, time
import pytz

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
LOAD_TEMPLATE_TAGS = "{% load volunteering_tags %}"

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
    from_address = models.CharField(default=settings.FROM_ADDRESS,
                                    max_length=255)
    bcc_address = models.EmailField(
        null=True, blank=True,
        help_text="BCC selected campaign emails to this address.")
    events = models.ManyToManyField('Event', blank=True,
                                    limit_choices_to={'is_archived': False})
    locations = models.ManyToManyField('Location', blank=True)
    activities = models.ManyToManyField('Activity', blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def deactivate(self):
        self.status = ActivatorModel.INACTIVE_STATUS
        self.deactivate_date = datetime_now()

    def duties(self):
        return Duty.objects.in_campaign(self).distinct()

    def duties_within_timespan(self, start, end):
            days_before_event = F('event__add_days_before_event')
            return self.duties() \
                       .filter(event__date__gte=start + days_before_event) \
                       .filter(event__date__lte=end + days_before_event)

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
            raise ValueError("If unassigned, then neither assigned \
                             nor assignable should be true.")
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
    EMAIL, SMS = range(2)
    MODES = (
        (EMAIL, 'email'),
        (SMS, 'sms'),
    )

    name = models.CharField(max_length=200)
    mode = models.IntegerField(choices=MODES, default=EMAIL)
    subject = models.CharField(max_length=200,
                               help_text="not used for SMS")
    body = models.TextField(blank=True)
    body_is_html = models.BooleanField(
        default=False,
        help_text="not used for SMS")

    def _render(self, source, context_dict):
        source = LOAD_TEMPLATE_TAGS + source
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
        return "%s (%s)" % (self.name, self.get_mode_display())


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
    send_to_bcc_address = models.BooleanField(default=True)

    class Meta:
        ordering = ['campaign']
        abstract = True

    def __unicode__(self):
        return "%s: %s" % (self.campaign, self.message)

    def recipients(self):
        raise NotImplementedError

    def bcc(self):
        base = settings.BCC_ADDRESSES or []
        if self.campaign.bcc_address and self.send_to_bcc_address:
            return base + [self.campaign.bcc_address]
        return base


class TriggerWithAssignmentStateMixin(models.Model):

    class Meta:
        abstract = True

    def _for_assigned(self):
        return self.assignment_state == TriggerBase.ASSIGNED or \
            self.assignment_state == TriggerBase.ASSIGNED_AND_ASSIGNABLE

    def _for_assignable(self):
        return self.assignment_state == TriggerBase.ASSIGNABLE or \
            self.assignment_state == TriggerBase.ASSIGNED_AND_ASSIGNABLE

    def _for_unassigned(self):
        return self.assignment_state == TriggerBase.UNASSIGNED

    def recipients(self):
            return self.campaign.recipients(
                assigned=self._for_assigned(),
                assignable=self._for_assignable(),
                unassigned=self._for_unassigned())


class DateTriggerQuerySet(models.QuerySet):
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


class TriggerByAssignment(TriggerBase):
    days_after = models.PositiveIntegerField(
        help_text="Send the message this many days after the role "
                  "was assigned to the volunteer (including them assigning "
                  "it themself). '0' will send the day they are assigned.")


class TriggerByEvent(TriggerWithAssignmentStateMixin, TriggerBase):
    days_before = models.PositiveIntegerField(
        help_text="Send the message this many days before the event.")
    assignment_state = models.IntegerField(
        choices=((TriggerBase.ASSIGNED, 'With an assigned duty'),),
        default=TriggerBase.ASSIGNED)


class TriggerByDate(TriggerWithAssignmentStateMixin, TriggerBase):

    fixed_date = models.DateField(
        null=True, blank=True, db_index=True,
        help_text="Send the message on this specific day. If today "
                  "or earlier the message will go immediately")
    assignment_state = models.IntegerField(
        choices=TriggerBase.ASSIGNMENT_STATES,
        default=TriggerBase.ASSIGNED_AND_ASSIGNABLE)

    objects = DateTriggerQuerySet.as_manager()


class Family(models.Model):
    REGENT_SUITE, SHUL, BOTH = (1, 2, 3)
    SERVICE_LOCATIONS = (
        (REGENT_SUITE, 'Regent Suite'),
        (SHUL, 'Shul'),
        (BOTH, 'Both'),
    )
    external_id = models.CharField(max_length=200, unique=True)
    hh_location = models.IntegerField(choices=SERVICE_LOCATIONS,
                                      null=True, blank=True)

    class Meta:
        ordering = ['external_id']
        verbose_name_plural = "Families"

    def __unicode__(self):
        return self.external_id

    def surnames(self):
        surnames = self.volunteer_set.order_by('surname').distinct(
            ).values_list('surname', flat=True)
        return ", ".join(surnames)

    def names(self):
        names = [v.name() for v in self.volunteer_set.all()]
        return ", ".join(sorted(names))

    def related_label(self):
        return u"%s (%s)" % (self.names(), self.external_id)


class Volunteer(TimeStampedModel):
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
    attributes = models.ManyToManyField(Attribute, blank=True)
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
        return "%s %s" % (self.dear_name or self.first_name, self.surname)

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

    def contact_methods(self):
        methods = []
        if self.home_phone != "":
            methods.append("home: %s" % self.home_phone)
        if self.mobile_phone != "":
            methods.append("mobile: %s" % self.mobile_phone)
        if self.email_address != "":
            methods.append(self.email_address)
        return methods

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

    def ordered_assignments(self):
        return self.assignment_set.all().order_by("-duty__event__date",
                                                  "-duty__start_time")

    def assignments_list(self):
        return 'hello'


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    add_days_before_event = models.IntegerField(default=0)
    web_summary_description = models.TextField(blank=True, default="")
    assignment_message_description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(
        default=True, db_index=True, help_text="Not available to volunteers.")
    is_archived = models.BooleanField(
        default=False, db_index=True,
        help_text="Exclude from future campaigns.")

    class Meta:
        unique_together = (("name", "date"))
        ordering = ['date']

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date)

    def create_deep_copy(self):
        copy = Event(
            name=self.name,
            web_summary_description=self.web_summary_description,
            assignment_message_description=self.assignment_message_description,
            add_days_before_event=self.add_days_before_event
        )
        copy.save()
        for duty in self.duty_set.all():
            duty.copy_for_event(copy)

    def get_absolute_url(self):
        return reverse('volunteering:event_report',
                       kwargs={'event_id': self.id})


class Activity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    web_summary_description = models.TextField(blank=True, default="")
    assignment_message_description = models.TextField(blank=True, default="")
    attributes = models.ManyToManyField(Attribute, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return self.name

    def attributes_list(self):
        return ", ".join(self.attributes.values_list('name', flat=True))


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    web_summary_description = models.TextField(blank=True, default="")
    assignment_message_description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class DutyManager(models.Manager):

    def _in_campaign_q(self, campaign):
        q_objects = []

        if campaign.events.exists():
            q_objects.append(Q(event__campaign=campaign))
            q_objects.append(Q(event__is_active=True))

        if campaign.locations.exists():
            q_objects.append(Q(location__campaign=campaign))

        if campaign.activities.exists():
            q_objects.append(Q(activity__campaign=campaign))

        return Q(*q_objects)

    def assignable_to(self, volunteer, as_of_date=None):
        if as_of_date is None:
            as_of_date = date.today()

        return (
            super(DutyManager, self).
            get_queryset().
            annotate(num_assignments=Count('assignments')).
            filter(num_assignments__lt=F('multiple')).
            filter(multiple__gt=0).
            filter(Q(event__is_active=True) |
                   Q(event__is_active__isnull=True)).
            filter(Q(event__date__gte=as_of_date) |
                   Q(event__date__isnull=True)).
            filter(Q(activity__attributes__volunteer=volunteer) |
                   Q(activity__attributes__isnull=True)).
            exclude(assignment__volunteer=volunteer)
        )

    def upcoming_assigned_to(self, volunteer, as_of_date=None):
        if as_of_date is None:
            as_of_date = date.today()

        return super(DutyManager, self).get_queryset(). \
            filter(assignment__volunteer=volunteer). \
            filter(Q(event__is_active=True) |
                   Q(event__is_active__isnull=True)). \
            filter(Q(event__date__gte=as_of_date) |
                   Q(event__date__isnull=True))

    def assigned_to(self, volunteer):
        return super(DutyManager, self).get_queryset(). \
            filter(assignment__volunteer=volunteer)

    def assignable_to_in_campaign(self, campaign, volunteer, as_of_date=None):
        return self.assignable_to(volunteer, as_of_date). \
            filter(self._in_campaign_q(campaign))

    def assigned_to_in_campaign(self, campaign, volunteer):
        return self.assigned_to(volunteer). \
            filter(self._in_campaign_q(campaign))

    def in_campaign(self, campaign):
        return super(DutyManager, self).get_queryset(). \
            filter(self._in_campaign_q(campaign))


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

    objects = DutyManager()

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
            name += " on " + self.event.name + \
                    " (" + str(self.event.date) + ")"
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

    def assigned_volunteers(self):
        return list(Volunteer.objects.filter(assignment__duty=self))

    def unassigned_count(self):
        return self.multiple - self.assignment_set.count()

    def has_multiple_volunteers(self):
        return Volunteer.objects.filter(assignment__duty=self).count() > 1

    def copy_for_event(self, event):
        Duty(activity=self.activity,
             event=event,
             location=self.location,
             start_time=self.start_time,
             end_time=self.end_time,
             multiple=self.multiple,
             details=self.details,
             coordinator_note=self.coordinator_note).save()

    def event_is_active(self):
        return self.event and self.event.is_active
    event_is_active.boolean = True


class AssignmentManager(models.Manager):
    def to_send_for_duties(self, duties, trigger_id, trigger_content_type):
        return super(AssignmentManager, self).get_queryset() \
            .filter(duty__in=duties) \
            .exclude(sendable__assignment_id=F('id'),
                     sendable__volunteer=F('volunteer'),
                     sendable__trigger_id=trigger_id,
                     sendable__trigger_type=trigger_content_type)


class Assignment(TimeStampedModel):
    volunteer = models.ForeignKey(Volunteer, db_index=True)
    duty = models.ForeignKey(Duty, db_index=True)
    assigned_location = models.ForeignKey(Location, null=True, blank=True,
                                          db_index=True)

    objects = AssignmentManager()

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
        return self.volunteer.family.get_hh_location_display()

    def duty_link(self):
        return '<a href="%s">%s</a>' % (
            reverse("admin:volunteering_duty_change", args=(self.duty_id,)),
            escape(str(self.duty)))
    duty_link.allow_tags = True
    duty_link.short_description = "Duty"

    def actual_location(self):
        if self.assigned_location is None:
            return self.duty.location
        return self.assigned_location


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

    def get_absolute_url(self):
        return reverse(
            'volunteering:email_content',
            kwargs={'sendable_id': self.id})

    def trigger_detail(self):
        return str(self.trigger)

    @classmethod
    def create_or_ignore(cls, trigger, volunteer, assignment, send_date):
        trigger_content_type = ContentType.objects.get_for_model(trigger)

        # create a sendable undless it already exists.
        s, created = Sendable.objects.get_or_create(
            trigger_id=trigger.id, trigger_type=trigger_content_type,
            volunteer=volunteer, assignment=assignment,
            send_date=send_date)

        # and note if it was created.
        if created:
            logger.info("Collected '%s'" % s)
        return created

    @classmethod
    def collect_from_event_only_assigned_triggers(cls, as_of_date,
                                                  verbose=False):
        new_sendables_count = 0
        today = date.today()

        for t in TriggerByEvent.objects.all():
            if verbose:
                print("Collecting event trigger: %s" % t)
            applicable_event_date = as_of_date + timedelta(days=t.days_before)
            trigger_content_type = ContentType.objects.get_for_model(t)
            campaign_duties = t.campaign.duties_within_timespan(
                today, applicable_event_date)
            assignments = Assignment.objects.to_send_for_duties(
                campaign_duties, t.id, trigger_content_type
                ).filter(duty__event__date__gte=as_of_date)

            for assignment in assignments:
                if verbose:
                    print("  Collecting assignment %s" % assignment)
                if Sendable.create_or_ignore(t, assignment.volunteer,
                                             assignment, as_of_date):
                    new_sendables_count += 1
        return new_sendables_count

    @classmethod
    def _duty_and_trigger_has_to_send(cls, trigger, volunteer):
        campaign = trigger.campaign
        if trigger.assignment_state == TriggerBase.ASSIGNED:
            return (Duty.
                    objects.assigned_to_in_campaign(campaign, volunteer).
                    exists())
        elif trigger.assignment_state == TriggerBase.ASSIGNABLE:
            return (Duty.objects.
                    assignable_to_in_campaign(campaign, volunteer).
                    exists())
        elif trigger.assignment_state == TriggerBase.ASSIGNED_AND_ASSIGNABLE:
            return (Duty.objects.assigned_to_in_campaign(campaign, volunteer).
                    exists()
                    or
                    Duty.
                    objects.assignable_to_in_campaign(campaign, volunteer).
                    exists()
                    )
        elif trigger.assignment_state == TriggerBase.UNASSIGNED:
            return (
                (not Duty.objects.
                    assigned_to_in_campaign(campaign, volunteer).
                    exists())
                and
                Duty.objects.
                assignable_to_in_campaign(campaign, volunteer).
                exists()
            )
        else:
            raise ValueError("Trigger assignment state \
                             not handled by Sendable.")

    @classmethod
    def collect_from_fixed_triggers(cls, fixed_date, verbose=False):
        new_sendables_count = 0

        triggers = TriggerByDate.objects.triggered(fixed_date).distinct()
        for t in triggers:
            if verbose:
                print("Collecting fixed date trigger: %s" % t)

            for volunteer in t.recipients():
                if verbose:
                    print("  Collecting %s" % volunteer)
                if Sendable._duty_and_trigger_has_to_send(t, volunteer):
                    if Sendable.create_or_ignore(t, volunteer, None,
                                                 fixed_date):
                        new_sendables_count += 1
        return new_sendables_count

    @classmethod
    def collect_from_assignment(cls, fixed_date, verbose=False):
        new_sendables_count = 0

        triggers = TriggerByAssignment.objects.all()
        for trigger in triggers:
            on_date = fixed_date - timedelta(trigger.days_after)
            on_datetime = datetime.combine(on_date, time(0, 0, 0, 0, pytz.utc))
            for assignment in Assignment.objects.filter(
                    duty__event__campaign=trigger.campaign
            ).filter(
                created__gte=on_datetime, created__lt=on_datetime+timedelta(1)
            ).filter(duty__event__date__gte=fixed_date):
                if Sendable.create_or_ignore(trigger, assignment.volunteer,
                                             assignment, fixed_date):
                    new_sendables_count += 1

        return new_sendables_count

    @classmethod
    def collect_all(cls, fixed_date, my_stdout, verbose=False):
        total = 0

        count = Sendable.collect_from_fixed_triggers(fixed_date, verbose)
        if verbose:
            my_stdout.write("Collected fixed date triggers: %d\n" % count)
        total += count

        count = Sendable.collect_from_assignment(fixed_date, verbose)
        if verbose:
            my_stdout.write("Collected assignment triggers: %d\n" % count)
        total += count

        count = Sendable.collect_from_event_only_assigned_triggers(fixed_date,
                                                                   verbose)
        if verbose:
            my_stdout.write("Collected event triggers: %d\n" % count)
        total += count

        if verbose:
            my_stdout.write("%s messages collected\n" % total)
        return total

    @classmethod
    def send_unsent(self, verbose=False):
        sent_count = 0
        for unsent in Sendable.objects.filter(
                sent_date__isnull=True).filter(send_failed=False):
            if unsent.send_email(verbose):
                sent_count += 1
        return sent_count

    def _email_context_dict(self):
        duty = getattr(self.assignment, 'duty', None)
        event = getattr(duty, 'event', None)
        activity = getattr(duty, 'activity', None)
        if self.assignment is not None:
            location = self.assignment.actual_location()
        else:
            location = None

        return {'volunteer': self.volunteer,
                'assignment': self.assignment,
                'duty': duty,
                'event': event,
                'activity': activity,
                'location': location, }

    def email_body(self):
        return self.trigger.message.rendered_body(self._email_context_dict())

    def send_email(self, verbose=False):
        # Return whether or not the sendable was sent.

        message = self.trigger.message
        body = self.email_body()

        email_params = {
            'subject': message.rendered_subject(self._email_context_dict()),
            'to': [self.volunteer.email_address],
            'bcc': self.trigger.bcc(),
            'from_email': self.trigger.campaign.from_address,
        }

        if message.body_is_html:
            email = EmailMultiAlternatives(**email_params)
            email.attach_alternative(body, "text/html")
            email.auto_text = True
        else:
            email = EmailMessage(**email_params)
            email.body = body
            email.auto_html = True

        # Tags are a mandril feature.
        name_tag = ("name - %s" % message.name)[:50]
        trigger_tag = ("trigger - %s" % self.trigger.id)[:50]
        email.tags = [name_tag, trigger_tag]
        logger.info("Sending %s" % email_params)
        if verbose:
            print("Sending %s" % email_params)
        try:
            email.send(fail_silently=False)
            self.sent_date = date.today()
        except MandrillAPIError:
            print("FAILED %s" % email_params)
            self.send_failed = True
        self.save()
        return not self.send_failed
