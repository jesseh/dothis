from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from volunteering.models import Campaign, Duty, Volunteer


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
        context = super(SummaryView, self).get_context_data(**kwargs)
        context['campaigns'] = Campaign.objects.all()
        context['volunteer'] = Volunteer.objects.get(slug=kwargs['volunteer_slug'])
        return context

class DutyView(TemplateView):

    template_name = 'volunteering/duty.html'

    def get_context_data(self, **kwargs):
        context = super(DutyView, self).get_context_data(**kwargs)

        volunteer = Volunteer.objects.get(slug=kwargs['volunteer_slug'])
        duty = Duty.objects.get(slug=kwargs['duty_slug'])

        context['volunteer'] = volunteer
        context['duty'] = duty
        context['is_claimed'] = volunteer.has_claimed(duty)
        return context

    def post(self, request, *args, **kwargs):
        volunteer = Volunteer.objects.get(slug=kwargs['volunteer_slug'])
        duty = Duty.objects.get(slug=kwargs['duty_slug'])

        volunteer.duty_set.add(duty)
        return redirect(request.path, permanent=False)