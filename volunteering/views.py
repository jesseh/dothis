from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from django_extensions.db.models import ActivatorModel

from volunteering.models import (Assignment, Campaign, CampaignDuty, Duty,
                                 Volunteer)


def importer(request):
    if request.method == 'POST':
        lines = request.POST['csv'].splitlines()

        created_count = 0
        updated_count = 0
        for line in lines:
            created = _get_or_create_volunteer(line)
            if created:
                created_count += 1
            else:
                updated_count += 1
        messages.success(request, '%s volunteers created and %s updated.' %
                         (created_count, updated_count))
        return redirect('/admin/volunteering/volunteer/')
    else:
        return render(request, 'volunteering/import.html')


def _get_or_create_volunteer(line):
    parts = [part.strip() for part in line.split(',')]
    external_id = parts[0]
    name = " ".join(parts[1:3])
    phone = parts[3]

    v, created = Volunteer.objects.get_or_create(external_id=external_id)
    v.name = name
    v.phone_number = phone
    v.save()
    return created


class SummaryView(TemplateView):

    template_name = 'volunteering/summary.html'

    def get_context_data(self, **kwargs):
        volunteer_slug = kwargs['volunteer_slug']

        context = super(SummaryView, self).get_context_data(**kwargs)

        volunteer = Volunteer.objects.get(slug=volunteer_slug)
        context['volunteer'] = volunteer
        assigned = Assignment.objects.filter(
            volunteer__slug=volunteer_slug).filter(
            campaign_duty__campaign__status=ActivatorModel.ACTIVE_STATUS)

        all_assignable = CampaignDuty.objects.filter(
            assignment__isnull=True).filter(
                campaign__status=ActivatorModel.ACTIVE_STATUS).filter(
                    Q(duty__attributes__volunteer=volunteer) |
                    Q(duty__attributes__isnull=True)
                ).order_by('campaign_id', 'duty_id').distinct('campaign_id',
                                                              'duty_id')
        assigned_keys = [(a.campaign_duty.campaign_id, a.campaign_duty.duty_id)
                         for a in assigned]
        assignable = [cd for cd in all_assignable
                      if not (cd.campaign_id, cd.duty_id) in assigned_keys]
        context['assigned'] = assigned
        context['assignable'] = assignable
        return context


class AssignmentView(TemplateView):

    template_name = 'volunteering/assignment.html'

    def get_context_data(self, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)

        volunteer = Volunteer.objects.get(slug=kwargs['volunteer_slug'])
        campaign = Campaign.objects.get(slug=kwargs['campaign_slug'])
        duty = Duty.objects.get(id=kwargs['duty_id'])

        context['volunteer'] = volunteer
        context['duty'] = duty
        context['is_claimed'] = volunteer.has_claimed(campaign, duty)
        return context

    def post(self, request, *args, **kwargs):
        volunteer_slug = kwargs['volunteer_slug']
        campaign_slug = kwargs['campaign_slug']
        duty_id = kwargs['duty_id']

        volunteer = Volunteer.objects.get(slug=volunteer_slug)
        campaign_duty = CampaignDuty.objects.filter(
            campaign__slug=campaign_slug,
            duty__id=duty_id,
            assignment__isnull=True
        )[:1].get()

        Assignment.objects.create(volunteer=volunteer,
                                  campaign_duty=campaign_duty)
        return redirect(volunteer.get_absolute_url(), permanent=False)
