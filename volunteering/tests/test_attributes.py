import unittest

from volunteering.models import Attribute, Campaign, Duty, Volunteer


class TestAttribute(unittest.TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        Attribute(name='yada').save()
        with self.assertRaises(Exception):
            Attribute(name='yada').save()


class TestVolunteer(unittest.TestCase):
    def testSettingAnAttribute(self):
        v = Volunteer.objects.create(name='tester')
        v.attributes.create(name='attr2')
        self.assertEqual('attr2', v.attributes.all()[0].name)

    def testHasAUniqueSlugThatHas8PlusOneChars(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual(9, len(v.slug))

    def testHasSlugWithDashInTheMiddle(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual('-', v.slug[4])

    def testTheSlugIsUnique(self):
        v1 = Volunteer.objects.create(name='tester')
        v2 = Volunteer.objects.create(name='tester2')
        self.assertNotEqual(v1.slug, v2.slug)


class TestDuty(unittest.TestCase):
    def testSettingAnAttribute(self):
        c = Campaign.objects.create(name='a campaign')
        d = Duty.objects.create(name='a duty', campaign=c)
        d.attributes.create(name='attr')
        self.assertEqual('attr', d.attributes.all()[0].name)

    def testHasSlug(self):
        d = Duty(slug='a slug')
        self.assertEqual('a slug', d.slug)


class TestCampaign(unittest.TestCase):
    def testHasSlug(self):
        c = Campaign(slug='a slug')
        self.assertEqual('a slug', c.slug)
