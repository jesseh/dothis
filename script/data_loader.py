"""

"""


from datetime import date
event_names = [
    ("Chol Ha'Moed Shabbat",               date(2014, 10, 11)),
    ("Erev Rosh HaShanah",                 date(2014, 9, 25)),
    ("Erev Rosh HaShanah 2",               date(2014, 9, 24)),
    ("Erev Shabbat - Shabbat Shuvah",      date(2014, 9, 26)),
    ("Erev Shabbat Bereishit",             date(2014, 10, 17)),
    ("Erev Shmini Atzeret",                date(2014, 10, 15)),
    ("Erev Simchat Torah",                 date(2014, 10, 16)),
    ("Erev Succot 1",                      date(2014, 10, 8)),
    ("Kol Nidrei",                         date(2014, 10, 3)),
    ("Rosh HaShanah 1",                    date(2014, 9, 25)),
    ("Rosh HaShanah 2",                    date(2014, 9, 26)),
    ("Shabbat Bereishit",                  date(2014, 10, 18)),
    ("Shabbat Shuvah",                     date(2014, 9, 27)),
    ("Shmini Atzeret",                     date(2014, 10, 16)),
    ("Simchat Torah",                      date(2014, 10, 17)),
    ("Succot 1",                           date(2014, 10, 9)),
    ("Succot 1, Erev Succot 2",            date(2014, 10, 9)),
    ("Succot 2",                           date(2014, 10, 10)),
    ("Succot 2/Erev Chol Ha'Moed Shabbat", date(2014, 10, 10)),
    ("Yom Kippur",                         date(2014, 10, 4)),
]

for e in event_names:
    Event.objects.get_or_create(name=e[0], date=e[1])

activities = [
    'Security supervising',
    'Security team member',
    'Stewarding',
]

for a in activities:
    Activity.objects.get_or_create(name=a)

locations = [
    'Sternberg Centre',
    'Regent Suite',
    'Hall Pavilion',
]

for l in locations:
    Location.objects.get_or_create(name=l)
