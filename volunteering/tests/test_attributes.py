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

    def testHasAUniqueObscureSlugThatHas8PlusOneChars(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual(9, len(v.obscure_slug))

    def testHasObscureSlugWithDashInTheMiddle(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual('-', v.obscure_slug[4])

    def testTheObscureSlugIsUnique(self):
        v1 = Volunteer.objects.create(name='tester')
        v2 = Volunteer.objects.create(name='tester2')
        self.assertNotEqual(v1.obscure_slug, v2.obscure_slug)


class TestDuty(unittest.TestCase):
    def testSettingAnAttribute(self):
        c = Campaign.objects.create(name='a campaign')
        d = Duty.objects.create(name='a duty', campaign=c)
        d.attributes.create(name='attr')
        self.assertEqual('attr', d.attributes.all()[0].name)
