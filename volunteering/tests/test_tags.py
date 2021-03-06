from django.template import Template, Context
from django.test import TestCase

import factories as f

# import volunteering.models as m


class TestEventReport(TestCase):
    def testEventReport_RendersTheEventName_GivenAnEvent(self):
        event = f.EventFactory.build()
        template = Template(
            "{% load volunteering_tags %} {% event_report event %}")
        rendered = template.render(Context({'event': event}))
        self.assertIn('Event report', rendered)

    def testEventReport_RendersAllVolunteerNamesRelatedToTheEvent(self):
        v1, v2 = f.VolunteerFactory.create_batch(2)
        event = f.EventFactory()
        duty = f.DutyFactory(event=event)
        f.AssignmentFactory(volunteer=v1, duty=duty)
        f.AssignmentFactory(volunteer=v2, duty=duty)
        template = Template(
            "{% load volunteering_tags %} {% event_report event %}")
        rendered = template.render(Context({'event': event}))
        self.assertIn(v1.first_name, rendered)
        self.assertIn(v2.first_name, rendered)

    def testEventReport_RendersMultipleDutiesAssociatedWithOneEvent(self):
        v1, v2 = f.VolunteerFactory.create_batch(2)
        event = f.EventFactory()
        duty1, duty2 = f.DutyFactory.create_batch(2, event=event)
        f.AssignmentFactory(volunteer=v1, duty=duty1)
        f.AssignmentFactory(volunteer=v2, duty=duty2)
        template = Template(
            "{% load volunteering_tags %} {% event_report event %}")
        rendered = template.render(Context({'event': event}))
        self.assertIn(v1.first_name, rendered)
        self.assertIn(v2.first_name, rendered)


class TestVolunteeredFor(TestCase):
    def testVolunteeredFor_ListsAllFutureAssignmentsForAVolunteer(self):
        event1 = f.EventFactory(name="e1name")
        event2 = f.EventFactory(name="e2name")
        event3 = f.EventFactory(name="e3name")
        volunteer = f.VolunteerFactory()
        duty1 = f.DutyFactory(event=event1)
        duty2 = f.DutyFactory(event=event2)
        f.AssignmentFactory(volunteer=volunteer, duty=duty1)
        f.AssignmentFactory(volunteer=volunteer, duty=duty2)
        template = Template(
            "{% load volunteering_tags %} {% volunteered_for volunteer %}")
        rendered = template.render(Context({'volunteer': volunteer}))
        self.assertIn(event1.name, rendered)
        self.assertIn(event2.name, rendered)
        self.assertNotIn(event3.name, rendered)


class TestAssignmentDetail(TestCase):
    def testAssignmentDetail_SaysTheDetails(self):
        event = f.EventFactory.build(name="yada")
        volunteer = f.VolunteerFactory.build()
        duty = f.DutyFactory.build(event=event)
        assignment = f.AssignmentFactory.build(volunteer=volunteer, duty=duty)
        template = Template(
            "{% load volunteering_tags %} {% assignment_detail assignment %}")
        rendered = template.render(Context({'assignment': assignment}))
        self.assertIn(event.name, rendered)


class TestDutyVolunteers(TestCase):
    def testDutyVolunteers_SaysTheVolunteers(self):
        event = f.EventFactory(name="yada")
        v1, v2 = f.VolunteerFactory.create_batch(2)
        duty = f.DutyFactory(event=event)
        f.AssignmentFactory(volunteer=v1, duty=duty)
        f.AssignmentFactory(volunteer=v2, duty=duty)

        template = Template(
            "{% load volunteering_tags %} {% duty_volunteers duty %}")
        rendered = template.render(Context({'duty': duty}))
        self.assertIn(v1.name(), rendered)
        self.assertIn(v2.name(), rendered)

    def testDutyVolunteers_SaysNothingIfOnlyOneVolunteer(self):
        event = f.EventFactory.build(name="yada")
        v1 = f.VolunteerFactory.build()
        duty = f.DutyFactory.build(event=event)
        f.AssignmentFactory.build(volunteer=v1, duty=duty)

        template = Template(
            "{% load volunteering_tags %} {% duty_volunteers duty %}")
        rendered = template.render(Context({'duty': duty}))
        self.assertEqual("", rendered.strip())
