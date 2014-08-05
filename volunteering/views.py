import csv
from StringIO import StringIO

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from volunteering.models import (Assignment, Duty, Volunteer, Family,
                                 Attribute)


def importer(request):
    if request.method == 'POST':
        data_file = StringIO(request.POST['csv'])
        data_csv = csv.DictReader(data_file, dialect=csv.excel_tab)

        created_count = 0
        updated_count = 0
        for record in data_csv:
            updated = _update_or_create_volunteer(record)
            if updated:
                updated_count += 1
            else:
                created_count += 1
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
    volunteer, updated = Volunteer.objects.update_or_create(params, external_id=record['MEMBER ID'])
    attribute_names = [a.strip() for a in record['ATTRIBUTES'].split(",")]
    volunteer.attributes.clear()
    for attribute_name in attribute_names:
        attribute = Attribute.objects.get(name=attribute_name)
        volunteer.attributes.add(attribute)

    volunteer.save()
    return updated


class SummaryView(TemplateView):

    template_name = 'volunteering/summary.html'

    def get_context_data(self, **kwargs):
        volunteer_slug = kwargs['volunteer_slug']

        context = super(SummaryView, self).get_context_data(**kwargs)

        volunteer = Volunteer.objects.get(slug=volunteer_slug)
        context['volunteer'] = volunteer
        assigned = Duty.objects.filter(assignment__volunteer=volunteer)
        all_assignable = Duty.objects.filter(
            assignment__isnull=True).filter(
                Q(activity__attributes__volunteer=volunteer) |
                Q(activity__attributes__isnull=True)
            ).distinct()
        assignable = list(set(all_assignable) - set(assigned))
        context['assigned'] = assigned
        context['assignable'] = assignable
        return context


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
        return redirect(volunteer.get_absolute_url(), permanent=False)
