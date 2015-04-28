import csv
from datetime import datetime
from StringIO import StringIO

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from volunteering.models import (Assignment, Duty, Volunteer, Family,
                                 Attribute, Event, Sendable)


def importer(request):
    if request.method == 'POST':
        data_file = StringIO(request.POST['csv'])
        data_csv = csv.DictReader(data_file, dialect=csv.excel_tab)

        created_count = 0
        updated_count = 0
        for record in data_csv:
            created = _update_or_create_volunteer(record)
            if created:
                created_count += 1
            else:
                updated_count += 1
        messages.success(request, '%s volunteers created and %s updated.' %
                         (created_count, updated_count))
        return redirect('/admin/volunteering/volunteer/')
    else:
        return render(request, 'volunteering/import.html')


def _update_or_create_volunteer(record):
    family, _ = Family.objects.get_or_create(external_id=record['FAMILY ID'])
    params = {
        'title': record['TITLE'],
        'first_name': record['FIRSTNAMES'],
        'surname': record['SURNAME'],
        'dear_name': record['DEARNAMES'],
        'external_id': record['MEMBER ID'],
        'family': family,
        'email_address': record['EMAIL'],
        'home_phone': record['HOME'],
        'mobile_phone': record['MOBILE'],
    }
    volunteer, created = Volunteer.objects.update_or_create(
        params, external_id=record['MEMBER ID'])
    # attribute_names = [a.strip() for a in record['ATTRIBUTES'].split(",")]
    # volunteer.attributes.clear()
    # for attribute_name in attribute_names:
    #     attribute = Attribute.objects.get(name=attribute_name)
    #     volunteer.attributes.add(attribute)

    # volunteer.save()
    return created


class SummaryView(TemplateView):

    template_name = 'volunteering/summary.html'

    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        volunteer = Volunteer.objects.get(slug=kwargs['volunteer_slug'])

        self.set_volunteer_last_view(volunteer)

        context['volunteer'] = volunteer
        context['assigned'] = Duty.objects.filter(
            assignment__volunteer=volunteer)
        context['assignable'] = Duty.objects.assignable_to(volunteer). \
            order_by('event', 'start_time').distinct()

        return context

    def set_volunteer_last_view(self, volunteer):
        volunteer.last_summary_view = timezone.now()
        volunteer.save()


class AssignmentView(TemplateView):

    template_name = 'volunteering/assignment.html'

    def get_context_data(self, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)

        volunteer = Volunteer.objects.get(slug=kwargs['volunteer_slug'])
        duty = Duty.objects.get(id=kwargs['duty_id'])

        context['volunteer'] = volunteer
        context['duty'] = duty
        context['is_claimed'] = volunteer.has_claimed(duty)
        return context

    def post(self, request, *args, **kwargs):
        volunteer_slug = kwargs['volunteer_slug']
        duty_id = kwargs['duty_id']

        volunteer = Volunteer.objects.get(slug=volunteer_slug)
        duty = Duty.objects.get(pk=duty_id)

        Assignment.objects.create(volunteer=volunteer, duty=duty)
        return redirect(request.path, permanent=False)


class EventReportView(TemplateView):

    template_name = 'volunteering/event_report.html'

    def get_context_data(self, **kwargs):
        context = super(EventReportView, self).get_context_data(**kwargs)

        event = Event.objects.get(id=kwargs['event_id'])

        context['event'] = event
        context['generated_datetime'] = datetime.now()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventReportView, self).dispatch(*args, **kwargs)


class EmailContentView(TemplateView):

    template_name = 'volunteering/email_content.html'

    def get_context_data(self, **kwargs):
        context = super(EmailContentView, self).get_context_data(**kwargs)

        sendable = Sendable.objects.get(id=kwargs['sendable_id'])

        context['body'] = sendable.email_body()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmailContentView, self).dispatch(*args, **kwargs)
