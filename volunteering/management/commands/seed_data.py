"""
Seed data in the database.
"""
import csv
from datetime import date, time
from StringIO import StringIO
from pprint import pformat

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_text

from volunteering.models import Event, Activity, Location, Attribute, Duty


class Command(BaseCommand):
    help = 'Load seed data into the database idempotently.'

    def handle(self, *args, **options):
        self.install_seed(Attribute, self.attribute_data())
        self.install_seed(Event, self.event_data())
        self.install_seed(Location, self.location_data())
        self.install_seed(Activity, self.activity_data())
        self.install_seed(Duty, self.duty_data())

    def install_seed(self, model, records):
        count = 0
        self.stdout.write('Loading data for %s' % model)
        for record in records:
            attributes = record.pop('attributes', [])
            instance, created = model.objects.update_or_create(**record)
            for attribute in attributes:
                instance.attributes.clear()
                instance.attributes.add(attribute)
            if created:
                count += 1
        self.stdout.write('%s new records created.' % count)

    def lookup_attributes(self, attribute_names):
        attributes = []
        for name in attribute_names:
            a = Attribute.objects.get(name=name)
            attributes.append(a)
        return attributes

    def event_data(self):
        return [
            {'name': "Chol Ha'Moed Shabbat", 'date': date(2014, 10, 11)},
            {'name': "Erev Rosh HaShanah", 'date': date(2014, 9, 25)},
            {'name': "Erev Rosh HaShanah 2", 'date': date(2014, 9, 24)},
            {'name': "Erev Shabbat - Shabbat Shuvah", 'date': date(2014, 9, 26)},
            {'name': "Erev Shabbat Bereishit", 'date': date(2014, 10, 17)},
            {'name': "Erev Shmini Atzeret", 'date': date(2014, 10, 15)},
            {'name': "Erev Simchat Torah", 'date': date(2014, 10, 16)},
            {'name': "Erev Succot 1", 'date': date(2014, 10, 8)},
            {'name': "Kol Nidrei", 'date': date(2014, 10, 3)},
            {'name': "Rosh HaShanah 1", 'date': date(2014, 9, 25)},
            {'name': "Rosh HaShanah 2", 'date': date(2014, 9, 26)},
            {'name': "Shabbat Bereishit", 'date': date(2014, 10, 18)},
            {'name': "Shabbat Shuvah", 'date': date(2014, 9, 27)},
            {'name': "Shmini Atzeret", 'date': date(2014, 10, 16)},
            {'name': "Simchat Torah", 'date': date(2014, 10, 17)},
            {'name': "Succot 1", 'date': date(2014, 10, 9)},
            {'name': "Succot 1, Succot 2", 'date': date(2014, 10, 9)},
            {'name': "Succot 2", 'date': date(2014, 10, 10)},
            {'name': "Succot 2/Erev Chol Ha'Moed Shabbat", 'date': date(2014, 10, 10)},
            {'name': "Yom Kippur", 'date': date(2014, 10, 4)},
        ]

    def attribute_data(self):
        return [
            {'name': 'security supervisor'},
            {'name': 'adult'},
            {'name': 'b\'nei mitzvah'},
        ]

    def activity_data(self):
        return [
            {'name': 'Security supervisor', 'attributes': self.lookup_attributes(['security supervisor'])},
            {'name': 'Security team member', 'attributes': self.lookup_attributes(['adult'])},
            {'name': 'Steward', 'attributes': self.lookup_attributes(['adult'])},
            {'name': 'Youth steward', 'attributes': self.lookup_attributes(['b\'nei mitzvah'])},
        ]


    def location_data(self):
        return [{'name': 'Sternberg Centre'},
                {'name': 'Regent Suite'},
                {'name': 'Hall Pavilion'},
                {'name': 'Manor House'},
                {'name': 'Akiva'},
                {'name': 'Shul hall'},
               ]

    def duty_data(self):
        data = csv.DictReader(self.duty_csv())
        records = []
        for duty in data:
            event = Event.objects.get(name=smart_text(duty['Event']))
            activity = Activity.objects.get(name=smart_text(duty['Activity']))
            location = Location.objects.get(name=smart_text(duty['Location']))
            record = {
                'event': event,
                'activity': activity,
                'location': location,
                'start_time': time(*([int(t) for t in duty['Start Time'].split(':')])),
                'end_time': time(*([int(t) for t in duty['End Time'].split(':')])),
                'multiple': int(duty['Multiple']),
                'coordinator_note': duty['Coordinator note'],
            }
            records.append(record)
        return records

    def duty_csv(self):
        return StringIO("""Event,Activity,Start Time,End Time,Multiple,Location,Coordinator note
Rosh HaShanah 1,Security supervisor,10:10,12:10,1,Hall Pavilion,
Yom Kippur,Security supervisor,10:40,12:40,1,Hall Pavilion,
Chol Ha'Moed Shabbat,Security supervisor,09:15,11:05,1,Manor House,
Chol Ha'Moed Shabbat,Security supervisor,10:55,13:00,1,Manor House,
Erev Shabbat Bereishit,Security supervisor,18:10,19:45,1,Manor House,
Rosh HaShanah 2,Security supervisor,07:45,09:15,1,Manor House,
Rosh HaShanah 2,Security supervisor,09:00,10:45,1,Manor House,
Rosh HaShanah 2,Security supervisor,10:30,12:15,1,Manor House,
Rosh HaShanah 2,Security supervisor,12:00,13:30,1,Manor House,
Shabbat Bereishit,Security supervisor,09:15,11:05,1,Manor House,
Shabbat Bereishit,Security supervisor,10:55,13:00,1,Manor House,
Shabbat Shuvah,Security supervisor,09:15,11:05,1,Manor House,
Shabbat Shuvah,Security supervisor,10:55,13:00,1,Manor House,
Shmini Atzeret,Security supervisor,09:15,11:05,1,Manor House,
Simchat Torah,Security supervisor,09:15,11:05,1,Manor House,
Simchat Torah,Security supervisor,10:55,13:00,1,Manor House,
Succot 1,Security supervisor,09:15,11:05,1,Manor House,
Succot 1,Security supervisor,10:55,13:00,1,Manor House,
Succot 1,Security supervisor,17:55,19:30,1,Manor House,
Succot 2,Security supervisor,09:15,11:05,1,Manor House,
Succot 2,Security supervisor,10:55,13:00,1,Manor House,
Erev Simchat Torah,Security supervisor,18:30,20:15,1,Manor House,Adult's service starts at 19:00
Erev Simchat Torah,Security supervisor,17:10,18:40,1,Manor House,Childrens service
Succot 2/Erev Chol Ha'Moed Shabbat,Security supervisor,18:10,19:45,1,Manor House,Service starts 18:30
Erev Shmini Atzeret,Security supervisor,17:40,19:00,1,Manor House,Service starts 18:00
Erev Succot 1,Security supervisor,17:55,19:30,1,Manor House,Service starts 18:15
Erev Rosh HaShanah 2,Security supervisor,18:00,19:45,1,Manor House,Service starts at 18:30 and lasts hour max
Erev Rosh HaShanah,Security supervisor,18:00,19:45,1,Manor House,Service starts at 18:30 and lasts hour max
Erev Shabbat - Shabbat Shuvah,Security supervisor,18:00,19:45,1,Manor House,Service starts 18:30
Rosh HaShanah 1,Security supervisor,07:45,09:15,2,Manor House,
Rosh HaShanah 1,Security supervisor,09:00,10:45,2,Manor House,
Rosh HaShanah 1,Security supervisor,10:30,12:15,2,Manor House,
Rosh HaShanah 1,Security supervisor,12:00,13:30,2,Manor House,could obviously end earlier if respective sites are cleared before 13:30
Kol Nidrei,Security supervisor,17:30,19:00,2,Manor House,"If RS start time should be later, you can advise those signed up and allocated there in due course"
Yom Kippur,Security supervisor,08:15,09:45,2,Manor House,
Yom Kippur,Security supervisor,09:30,11:15,2,Manor House,
Yom Kippur,Security supervisor,11:00,12:45,2,Manor House,
Yom Kippur,Security supervisor,12:30,14:30,2,Manor House,
Yom Kippur,Security supervisor,14:15,16:00,2,Manor House,
Yom Kippur,Security supervisor,15:45,17:45,2,Manor House,
Yom Kippur,Security supervisor,17:30,19:30,2,Manor House,
Kol Nidrei,Security supervisor,18:45,20:30,2,Manor House,
Kol Nidrei,Security supervisor,20:15,21:30,2,Manor House,
Rosh HaShanah 1,Security supervisor,07:45,09:15,1,Regent Suite,
Rosh HaShanah 1,Security supervisor,09:00,10:45,1,Regent Suite,
Rosh HaShanah 1,Security supervisor,10:30,12:15,1,Regent Suite,
Rosh HaShanah 1,Security supervisor,12:00,13:30,1,Regent Suite,could obviously end earlier if respective sites are cleared before 13:30
Kol Nidrei,Security supervisor,17:30,19:00,2,Regent Suite,"If RS start time should be later, you can advise those signed up and allocated there in due course"
Kol Nidrei,Security supervisor,18:45,20:30,2,Regent Suite,
Kol Nidrei,Security supervisor,20:15,21:30,2,Regent Suite,
Yom Kippur,Security supervisor,08:15,09:45,1,Regent Suite,
Yom Kippur,Security supervisor,09:30,11:15,1,Regent Suite,
Yom Kippur,Security supervisor,11:00,12:45,1,Regent Suite,
Yom Kippur,Security supervisor,12:30,14:30,1,Regent Suite,
Yom Kippur,Security supervisor,14:15,16:00,1,Regent Suite,
Yom Kippur,Security supervisor,15:45,17:45,1,Regent Suite,
Yom Kippur,Security supervisor,17:30,19:30,1,Regent Suite,
Rosh HaShanah 1,Security team member,10:10,12:10,1,Hall Pavilion,
Yom Kippur,Security team member,10:40,12:40,1,Hall Pavilion,
Erev Rosh HaShanah 2,Security team member,18:00,19:45,1,Manor House,
Erev Shabbat - Shabbat Shuvah,Security team member,18:00,19:45,1,Manor House,
Erev Shabbat Bereishit,Security team member,18:10,19:45,1,Manor House,
Erev Shmini Atzeret,Security team member,17:40,19:00,1,Manor House,
Erev Simchat Torah,Security team member,17:10,18:40,1,Manor House,
Erev Simchat Torah,Security team member,18:30,20:15,1,Manor House,
Erev Succot 1,Security team member,17:55,19:30,1,Manor House,
Succot 1,Security team member,17:55,19:30,1,Manor House,
Succot 2/Erev Chol Ha'Moed Shabbat,Security team member,18:10,19:45,1,Manor House,
Chol Ha'Moed Shabbat,Security team member,09:15,11:05,2,Manor House,
Chol Ha'Moed Shabbat,Security team member,10:55,13:00,2,Manor House,
Erev Rosh HaShanah,Security team member,18:00,19:45,2,Manor House,
Shabbat Bereishit,Security team member,09:15,11:05,2,Manor House,
Shabbat Bereishit,Security team member,10:55,13:00,2,Manor House,
Shabbat Shuvah,Security team member,09:15,11:05,2,Manor House,
Shabbat Shuvah,Security team member,10:55,13:00,2,Manor House,
Simchat Torah,Security team member,09:15,11:05,2,Manor House,
Simchat Torah,Security team member,10:55,13:00,2,Manor House,
Succot 1,Security team member,09:15,11:05,2,Manor House,
Succot 1,Security team member,10:55,13:00,2,Manor House,
Succot 2,Security team member,09:15,11:05,2,Manor House,
Succot 2,Security team member,10:55,13:00,2,Manor House,
Rosh HaShanah 2,Security team member,07:45,09:15,4,Manor House,
Rosh HaShanah 2,Security team member,09:00,10:45,4,Manor House,
Rosh HaShanah 2,Security team member,10:30,12:15,4,Manor House,
Rosh HaShanah 2,Security team member,12:00,13:30,4,Manor House,
Rosh HaShanah 1,Security team member,07:45,09:15,6,Manor House,
Yom Kippur,Security team member,08:15,09:45,3,Manor House,
Yom Kippur,Security team member,09:30,11:15,3,Manor House,
Yom Kippur,Security team member,15:45,17:45,3,Manor House,
Yom Kippur,Security team member,11:00,12:45,4,Manor House,
Yom Kippur,Security team member,12:30,14:30,4,Manor House,
Yom Kippur,Security team member,14:15,16:00,4,Manor House,
Yom Kippur,Security team member,17:30,19:30,5,Manor House,
Kol Nidrei,Security team member,17:30,19:00,6,Manor House,
Kol Nidrei,Security team member,18:45,20:30,6,Manor House,
Kol Nidrei,Security team member,20:15,21:30,6,Manor House,
Rosh HaShanah 1,Security team member,09:00,10:45,6,Manor House,
Rosh HaShanah 1,Security team member,10:30,12:15,6,Manor House,
Rosh HaShanah 1,Security team member,12:00,13:30,6,Manor House,could obviously end earlier if respective sites are cleared before 13:30
Rosh HaShanah 1,Security team member,07:45,09:15,3,Regent Suite,
Yom Kippur,Security team member,08:15,09:45,3,Regent Suite,
Yom Kippur,Security team member,09:30,11:15,3,Regent Suite,
Yom Kippur,Security team member,15:45,17:45,3,Regent Suite,
Yom Kippur,Security team member,11:00,12:45,4,Regent Suite,
Yom Kippur,Security team member,12:30,14:30,4,Regent Suite,
Yom Kippur,Security team member,14:15,16:00,4,Regent Suite,
Yom Kippur,Security team member,17:30,19:30,5,Regent Suite,
Kol Nidrei,Security team member,17:30,19:00,6,Regent Suite,
Kol Nidrei,Security team member,18:45,20:30,6,Regent Suite,
Kol Nidrei,Security team member,20:15,21:30,6,Regent Suite,
Rosh HaShanah 1,Security team member,09:00,10:45,6,Regent Suite,
Rosh HaShanah 1,Security team member,10:30,12:15,6,Regent Suite,
Rosh HaShanah 1,Security team member,12:00,13:30,6,Regent Suite,could obviously end earlier if respective sites are cleared before 13:30
Rosh HaShanah 1,Steward,08:15,09:45,3,Akiva,
Rosh HaShanah 2,Steward,08:15,09:45,3,Akiva,
Rosh HaShanah 2,Steward,09:45,11:15,5,Akiva,
Rosh HaShanah 2,Steward,11:15,13:15,5,Akiva,Obviously could finish sooner if services finish earlier
Rosh HaShanah 1,Steward,09:45,11:15,5,Akiva,
Rosh HaShanah 1,Steward,11:15,13:15,5,Akiva,
Erev Rosh HaShanah,Steward,18:20,19:45,1,Manor House,
Erev Rosh HaShanah 2,Steward,18:20,19:45,1,Manor House,
Erev Shabbat - Shabbat Shuvah,Steward,18:20,19:00,1,Manor House,
Erev Shabbat Bereishit,Steward,18:20,19:00,1,Manor House,
Erev Shmini Atzeret,Steward,17:50,18:30,1,Manor House,
Erev Simchat Torah,Steward,18:50,19:30,1,Manor House,
Erev Succot 1,Steward,18:05,19:00,1,Manor House,
Shabbat Shuvah,Steward,09:20,11:15,1,Manor House,
Simchat Torah,Steward,09:20,11:15,1,Manor House,
Succot 1,Steward,09:20,11:15,1,Manor House,
Succot 1,Steward,18:05,19:00,1,Manor House,
Succot 2,Steward,09:20,11:15,1,Manor House,
Succot 2/Erev Chol Ha'Moed Shabbat,Steward,18:15,19:00,1,Manor House,
Rosh HaShanah 1,Steward,10:45,12:30,3,Manor House,Help with Buggy Parking/Management before/during/after children's services (1 at GA entrance; 1 at MH/Circle; 1 outside Akiva)
Yom Kippur,Steward,10:45,12:30,3,Manor House, Help with Buggy Parking/Management before/during/after children's services (1 at GA entrance; 1 at MH/Circle; 1 outside Akiva
Rosh HaShanah 1,Steward,10:15,12:15,4,Manor House,
Yom Kippur,Steward,10:40,12:40,4,Manor House,
Yom Kippur,Steward,15:15,16:45,8,Manor House,Akiva-4; Shul-4
Yom Kippur,Steward,16:45,18:15,8,Manor House,Akiva-4; Shul-4
Yom Kippur,Steward,08:50,10:30,8,Manor House,Akiva-4; Shul-4
Yom Kippur,Steward,13:45,15:15,8,Manor House,Akiva-4; Shul-4
Yom Kippur,Steward,10:30,12:00,11,Manor House, Akiva:5; Shul: 6
Yom Kippur,Steward,12:15,13:45,11,Manor House, Akiva:5; Shul: 6
Yom Kippur,Steward,18:15,19:30,11,Manor House, Akiva:5; Shul: 6
Rosh HaShanah 1,Steward,08:15,09:45,3,Regent Suite,
Yom Kippur,Steward,15:15,16:45,4,Regent Suite,
Yom Kippur,Steward,16:45,18:15,4,Regent Suite,
Yom Kippur,Steward,08:50,10:30,5,Regent Suite,
Yom Kippur,Steward,13:45,15:15,5,Regent Suite,
Rosh HaShanah 1,Steward,09:45,11:15,6,Regent Suite,
Rosh HaShanah 1,Steward,11:15,13:15,6,Regent Suite,
Yom Kippur,Steward,10:30,12:00,6,Regent Suite,
Yom Kippur,Steward,12:15,13:45,6,Regent Suite,
Yom Kippur,Steward,18:15,19:30,6,Regent Suite,
Rosh HaShanah 2,Steward,10:45,12:30,3,Shul hall,Help with buggy parking/management as per RH1
Rosh HaShanah 2,Steward,08:15,09:45,4,Shul hall,
Rosh HaShanah 2,Steward,09:45,11:15,6,Shul hall,
Rosh HaShanah 2,Steward,11:15,13:15,6,Shul hall,Obviously could finish sooner if services finish earlier
Rosh HaShanah 1,Steward,09:45,11:15,6,Shul hall,
Rosh HaShanah 1,Steward,11:15,13:15,6,Shul hall,
Rosh HaShanah 1,Steward,08:15,09:45,4,Shul hall,
Kol Nidrei,Steward,18:00,19:30,11,Manor House,5 - Akiva; 6 - Shul
Kol Nidrei,Steward,19:30,21:15,11,Manor House,5 - Akiva; 6 - Shul
Kol Nidrei,Steward,18:00,19:30,11,Regent Suite,5 - Akiva; 6 - Shul
Kol Nidrei,Steward,19:30,21:15,11,Regent Suite,5 - Akiva; 6 - Shul
Chol Ha'Moed Shabbat,Youth steward,09:20,11:15,2,Manor House,
Shabbat Bereishit,Youth steward,09:15,11:15,2,Manor House,
""")
