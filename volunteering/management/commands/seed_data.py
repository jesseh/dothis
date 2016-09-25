"""
Seed data in the database.
"""
import csv
from datetime import date, time
from StringIO import StringIO

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
            {'name': "Erev Rosh HaShanah", 'date': date(2014, 9, 24)},
            {'name': "Erev Rosh HaShanah 2", 'date': date(2014, 9, 25)},
            {'name': "Erev Shabbat - Shabbat Shuvah",
             'date': date(2014, 9, 26)},
            {'name': "Erev Shabbat Bereishit", 'date': date(2014, 10, 17)},
            {'name': "Erev Shmini Atzeret", 'date': date(2014, 10, 15)},
            {'name': "Erev Simchat Torah", 'date': date(2014, 10, 16)},
            {'name': "Erev Succot 1", 'date': date(2014, 10, 8)},
            {'name': "Kol Nidrei", 'date': date(2014, 10, 3)},
            {'name': "Rosh HaShanah 1", 'date': date(2014, 9, 25)},
            {'name': "Rosh HaShanah 2", 'date': date(2014, 9, 26)},
            {'name': "Shabbat Bereishit", 'date': date(2014, 10, 17)},
            {'name': "Shabbat Shuvah", 'date': date(2014, 9, 27)},
            {'name': "Shmini Atzeret", 'date': date(2014, 10, 16)},
            {'name': "Simchat Torah", 'date': date(2014, 10, 17)},
            {'name': "Succot 1", 'date': date(2014, 10, 9)},
            {'name': "Succot 1, Succot 2", 'date': date(2014, 10, 9)},
            {'name': "Succot 2", 'date': date(2014, 10, 10)},
            {'name': "Succot 2/Erev Chol Ha'Moed Shabbat",
             'date': date(2014, 10, 10)},
            {'name': "Yom Kippur", 'date': date(2014, 10, 4)},
        ]

    def attribute_data(self):
        return [
            {'name': 'security supervisor'},
            {'name': 'security able'},
            {'name': 'greeter able'},
            {'name': 'adult'},
            {'name': 'senior'},
            {'name': 'b\'nei mitzvah'},
        ]

    def activity_data(self):
        return [
            {'name': 'Security supervisor',
             'attributes': self.lookup_attributes(['security supervisor'])},
            {'name': 'Security team member',
             'attributes': self.lookup_attributes(['security able'])},
            {'name': 'Greeter',
             'attributes': self.lookup_attributes(['greeter able'])},
            {'name': 'Youth greeter',
             'attributes': self.lookup_attributes(['b\'nei mitzvah'])},
        ]

    def location_data(self):
        return [{'name': 'Regent Suite'},
                {'name': 'Hall Pavilion'},
                {'name': 'Manor House'},
                {'name': 'Akiva'},
                {'name': 'Shul Hall'},
                {'name': 'To be determined'},
                {'name': 'location to be determined',
                 'web_summary_description': 'We need to recruit volunteers before the allocation of people to ' + \
                 'venues. As a result we\'ll align the locations at a later date and will let you ' + \
                 'know where to go then.'}
               ]

    def duty_data(self):
        data = csv.DictReader(self.duty_csv())
        records = []
        for duty in data:
            self.stdout.write(str(duty))
            event = Event.objects.get(name=smart_text(duty['Event']))
            activity = Activity.objects.get(name=smart_text(duty['Activity']))
            location = Location.objects.get(name=smart_text(duty['Location']))
            record = {
                'event': event,
                'activity': activity,
                'location': location,
                'start_time': time(*([int(t) for t in duty['Start Time']\
                        .split(':')])),
                'end_time': time(*([int(t) for t in duty['End Time'].split(':')])),
                'multiple': int(duty['Multiple']),
                'coordinator_note': duty['Coordinator note'],
            }
            records.append(record)
        return records

    def duty_csv(self):
        return StringIO("""Event,Start Time,End Time,Activity,Multiple,Location,Coordinator note
Chol Ha'Moed Shabbat,09:15,11:05,Security supervisor,1,To be determined,
Chol Ha'Moed Shabbat,09:15,11:05,Security team member,2,To be determined,
Chol Ha'Moed Shabbat,09:20,11:15,Youth greeter,2,To be determined,
Chol Ha'Moed Shabbat,10:55,13:00,Security supervisor,1,To be determined,
Chol Ha'Moed Shabbat,10:55,13:00,Security team member,2,To be determined,
Erev Rosh HaShanah 2,18:00,19:45,Security supervisor,1,To be determined,Service starts at 18:30 and lasts hour max
Erev Rosh HaShanah 2,18:00,19:45,Security team member,1,To be determined,
Erev Rosh HaShanah 2,18:20,19:45,Greeter,1,To be determined,
Erev Rosh HaShanah,18:00,19:45,Security supervisor,1,To be determined,Service starts at 18:30 and lasts hour max
Erev Rosh HaShanah,18:00,19:45,Security team member,2,To be determined,
Erev Shabbat - Shabbat Shuvah,18:00,19:45,Security supervisor,1,To be determined,Service starts 18:30
Erev Shabbat - Shabbat Shuvah,18:00,19:45,Security team member,1,To be determined,
Erev Shabbat - Shabbat Shuvah,18:20,19:00,Greeter,1,To be determined,
Erev Shabbat Bereishit,18:10,19:45,Security supervisor,1,To be determined,
Erev Shabbat Bereishit,18:10,19:45,Security team member,1,To be determined,
Erev Shabbat Bereishit,18:20,19:00,Greeter,1,To be determined,
Erev Shmini Atzeret,17:40,19:00,Security supervisor,1,To be determined,Service starts 18:00
Erev Shmini Atzeret,17:40,19:00,Security team member,1,To be determined,
Erev Shmini Atzeret,17:50,18:30,Greeter,1,To be determined,
Erev Simchat Torah,17:10,18:40,Security supervisor,1,To be determined,Childrens service
Erev Simchat Torah,17:10,18:40,Security team member,1,To be determined,
Erev Simchat Torah,18:30,20:15,Security supervisor,1,To be determined,Adult's service starts at 19:00
Erev Simchat Torah,18:30,20:15,Security team member,1,To be determined,
Erev Simchat Torah,18:50,19:30,Greeter,1,To be determined,
Erev Succot 1,17:55,19:30,Security supervisor,1,To be determined,Service starts 18:15
Erev Succot 1,17:55,19:30,Security team member,1,To be determined,
Erev Succot 1,18:05,19:00,Greeter,1,To be determined,
Kol Nidrei,17:30,19:00,Security supervisor,4,To be determined,"If RS start time should be later, you can advise those signed up and allocated there in due course"
Kol Nidrei,17:30,19:00,Security team member,15,To be determined,
Kol Nidrei,18:00,19:30,Greeter,17,To be determined,RS: 6; MH: 11 (5 - Akiva; 6 - Shul)
Kol Nidrei,18:45,20:30,Security supervisor,4,To be determined,MH:2; RS:2
Kol Nidrei,18:45,20:30,Security team member,15,To be determined,MH: 9; RS: 6
Kol Nidrei,19:30,21:15,Greeter,17,To be determined,RS: 6; MH: 11 (5 - Akiva; 6 - Shul)
Kol Nidrei,20:15,21:30,Security supervisor,4,To be determined,MH:2; RS:2
Kol Nidrei,20:15,21:30,Security team member,15,To be determined,MH: 9; RS: 6
Rosh HaShanah 1,07:45,09:15,Security supervisor,3,To be determined,MH: 2; RS: 1
Rosh HaShanah 1,07:45,09:15,Security team member,9,To be determined,MH: 6; RS: 3
Rosh HaShanah 1,08:15,09:45,Greeter,10,To be determined,Akiva: 3,Akiva: 3, Shul: 4; RS: 3
Rosh HaShanah 1,09:00,10:45,Security supervisor,3,To be determined,MH: 2; RS: 1
Rosh HaShanah 1,09:00,10:45,Security team member,15,To be determined,MH: 9; RS: 6
Rosh HaShanah 1,10:10,12:10,Security supervisor,1,To be determined,Hall Pavilion
Rosh HaShanah 1,10:10,12:10,Security team member,1,To be determined,Hall Pavilion
Rosh HaShanah 1,09:45,11:15,Greeter,17,To be determined,Akiva: 5; Shul: 6; RS: 6
Rosh HaShanah 1,10:15,12:15,Greeter,4,To be determined,MH - Beit Tefilah - Family Service (1) - Hall Pav: 2 - Explanatory Service (CM to liaise with ZSh)
Rosh HaShanah 1,10:45,12:30,Greeter,3,To be determined,Help with Buggy Parking/Management before/during/after children's services (1 at GA entrance; 1 at MH/Circle; 1 outside Akiva)
Rosh HaShanah 1,10:30,12:15,Security supervisor,3,To be determined,MH: 2; RS: 1
Rosh HaShanah 1,10:30,12:15,Security team member,15,To be determined,MH: 9; RS: 6
Rosh HaShanah 1,11:15,13:15,Greeter,17,To be determined,Akiva: 5; Shul: 6; RS: 6
Rosh HaShanah 1,12:00,13:30,Security supervisor,3,To be determined,could obviously end earlier if respective sites are cleared before 13:30
Rosh HaShanah 1,12:00,13:30,Security team member,15,To be determined,could obviously end earlier if respective sites are cleared before 13:30
Rosh HaShanah 2,07:45,09:15,Security supervisor,1,Manor House,
Rosh HaShanah 2,07:45,09:15,Security team member,4,Manor House,
Rosh HaShanah 2,08:15,09:45,Greeter,7,To be determined,Akiva: 3; Shul: 4
Rosh HaShanah 2,09:00,10:45,Security supervisor,1,Manor House,
Rosh HaShanah 2,09:00,10:45,Security team member,4,Manor House,
Rosh HaShanah 2,09:45,11:15,Greeter,11,To be determined,Akiva: 5; Shul: 6
Rosh HaShanah 2,10:45,12:30,Greeter,3,To be determined,Help with buggy parking/management as per RH1
Rosh HaShanah 2,10:30,12:15,Security supervisor,1,Manor House,
Rosh HaShanah 2,10:30,12:15,Security team member,4,Manor House,
Rosh HaShanah 2,11:15,13:15,Greeter,11,To be determined,Obviously could finish sooner if services finish earlier
Rosh HaShanah 2,12:00,13:30,Security supervisor,1,Manor House,
Rosh HaShanah 2,12:00,13:30,Security team member,4,Manor House,
Shabbat Bereishit,09:15,11:05,Security supervisor,1,To be determined,
Shabbat Bereishit,09:15,11:05,Security team member,2,To be determined,
Shabbat Bereishit,09:15,11:15,Youth greeter,2,To be determined,
Shabbat Bereishit,10:55,13:00,Security supervisor,1,To be determined,
Shabbat Bereishit,10:55,13:00,Security team member,2,To be determined,
Shabbat Shuvah,09:15,11:05,Security supervisor,1,To be determined,
Shabbat Shuvah,09:15,11:05,Security team member,2,To be determined,
Shabbat Shuvah,09:20,11:15,Greeter,1,To be determined,
Shabbat Shuvah,10:55,13:00,Security supervisor,1,To be determined,
Shabbat Shuvah,10:55,13:00,Security team member,2,To be determined,
Shmini Atzeret,09:15,11:05,Security supervisor,1,Manor House,
Shmini Atzeret,09:15,11:05,Security supervisor,1,Manor House,
Shmini Atzeret,09:15,11:05,Security team member,2,Manor House,
Shmini Atzeret,09:20,11:15,Greeter,1,Manor House,
Shmini Atzeret,10:55,13:00,Security supervisor,1,Manor House,
Shmini Atzeret,10:55,13:00,Security team member,2,Manor House,
Simchat Torah,09:15,11:05,Security supervisor,1,Manor House,
Simchat Torah,09:15,11:05,Security team member,2,Manor House,
Simchat Torah,09:20,11:15,Greeter,1,Manor House,
Simchat Torah,10:55,13:00,Security supervisor,1,Manor House,
Simchat Torah,10:55,13:00,Security team member,2,Manor House,
Succot 1,09:15,11:05,Security supervisor,1,To be determined,
Succot 1,09:15,11:05,Security team member,2,To be determined,
Succot 1,09:20,11:15,Greeter,1,To be determined,
Succot 1,10:55,13:00,Security supervisor,1,To be determined,
Succot 1,10:55,13:00,Security team member,2,To be determined,
Succot 1,17:55,19:30,Security supervisor,1,To be determined,
Succot 1,17:55,19:30,Security team member,1,To be determined,
Succot 1,18:05,19:00,Greeter,1,To be determined,
Succot 2,09:15,11:05,Security supervisor,1,Manor House,
Succot 2,09:15,11:05,Security team member,2,Manor House,
Succot 2,09:20,11:15,Greeter,1,Manor House,
Succot 2,10:55,13:00,Security supervisor,1,Manor House,
Succot 2,10:55,13:00,Security team member,2,Manor House,
Succot 2/Erev Chol Ha'Moed Shabbat,18:10,19:45,Security supervisor,1,Manor House, Service starts 18:30
Succot 2/Erev Chol Ha'Moed Shabbat,18:10,19:45,Security team member,1,Manor House,
Succot 2/Erev Chol Ha'Moed Shabbat,18:15,19:00,Greeter,1,Manor House,
Yom Kippur,08:15,09:45,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,08:15,09:45,Security team member,12,To be determined,MH: 9; RS: 3
Yom Kippur,08:50,10:30,Greeter,13,To be determined,MH: 8 (Akiva-4; Shul-4); RS: 5
Yom Kippur,09:30,11:15,Security supervisor,3,To be determined,MH:2; RS: 1,MH:2; RS: 1
Yom Kippur,09:30,11:15,Security team member,12,To be determined,
Yom Kippur,10:40,12:40,Security supervisor,1,To be determined,Hall pavilion
Yom Kippur,10:40,12:40,Security team member,1,To be determined,Hall pavilion
Yom Kippur,10:40,12:40,Greeter,4,To be determined,MH - Beit Tefilah - Family Service (1) - Hall Pav: 2 - Explanatory Service (CM to liaise with ZSh)
Yom Kippur,10:30,12:00,Greeter,17,To be determined, MH: 11 (Akiva:5; Shul: 6); RS: 6
Yom Kippur,10:45,12:30,Greeter,3,To be determined, Help with Buggy Parking/Management before/during/after children's services (1 at GA entrance; 1 at MH/Circle; 1 outside Akiva
Yom Kippur,11:00,12:45,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,11:00,12:45,Security team member,13,To be determined,MH: 9; RS: 4
Yom Kippur,12:15,13:45,Greeter,17,To be determined,MH: 11 (Akiva:5; Shul: 6); RS: 6
Yom Kippur,12:30,14:30,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,12:30,14:30,Security team member,13,To be determined,MH: 9; RS: 4
Yom Kippur,13:45,15:15,Greeter,13,To be determined,MH: 8 (Akiva-4; Shul-4); RS: 5
Yom Kippur,14:15,16:00,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,14:15,16:00,Security team member,13,To be determined,MH: 9; RS: 4
Yom Kippur,15:15,16:45,Greeter,12,To be determined,MH: 8 (Akiva-4; Shul-4); RS: 4
Yom Kippur,15:45,17:45,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,15:45,17:45,Security team member,12,To be determined,MH: 9; RS: 3
Yom Kippur,16:45,18:15,Greeter,12,To be determined,MH: 8 (Akiva-4; Shul-4); RS: 4
Yom Kippur,17:30,19:30,Security supervisor,3,To be determined,MH:2; RS: 1
Yom Kippur,17:30,19:30,Security team member,14,To be determined,MH: 9; RS: 5
Yom Kippur,18:15,19:30,Greeter,17,To be determined,MH: 11 (Akiva:5; Shul: 6); RS: 6
""")
