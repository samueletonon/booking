import datetime

today = datetime.datetime.now()
for x in range(200):
    y = today + datetime.timedelta(days=x)
    pp = Day(day=y.date())
    pp.save()
