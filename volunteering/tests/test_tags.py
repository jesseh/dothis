from django.template import Template, Context
from django.test import TestCase

import factories as f

# import volunteering.models as m


class TestEventReport(TestCase):
    def test_RendersTheEventName(self):
        assignment = f.AssignmentFactory()
        template = Template(
            "{% load volunteering_tags %} {% event_report assignment %}")
        rendered = template.render(Context({'assignment': assignment}))
        self.assertIn('Event report', rendered)

    def test_RendersAllTheVolunteerNamesRelatedToThatAssignmentAndDuty(self):
        v1, v2 = f.VolunteerFactory.create_batch(2)
        event = f.EventFactory()
        duty = f.DutyFactory(event=event)
        assignment = f.AssignmentFactory(volunteer=v1, duty=duty)
        f.AssignmentFactory(volunteer=v2, duty=duty)
        template = Template(
            "{% load volunteering_tags %} {% event_report assignment %}")
        rendered = template.render(Context({'assignment': assignment}))
        self.assertIn(v1.first_name, rendered)
        self.assertIn(v2.first_name, rendered)

    def test_RendersMultipleDutiesAssociatedWithOneEvent(self):
        v1, v2 = f.VolunteerFactory.create_batch(2)
        event = f.EventFactory()
        duty1, duty2 = f.DutyFactory.create_batch(2, event=event)
        assignment = f.AssignmentFactory(volunteer=v1, duty=duty1)
        f.AssignmentFactory(volunteer=v2, duty=duty2)
        template = Template(
            "{% load volunteering_tags %} {% event_report assignment %}")
        rendered = template.render(Context({'assignment': assignment}))
        self.assertIn(v1.first_name, rendered)
        self.assertIn(v2.first_name, rendered)
