import httpx
from icalendar import Calendar, Event, vDatetime, Timezone, Alarm
from parsel import Selector
from datetime import datetime, date, timedelta


url = "https://www.giantessfan.com/comics/pag=1/"

html = httpx.get(url).text

comic_name = Selector(html).css(".col-sm-6 a::text").getall()
comic_url = Selector(html).css(".col-sm-6 .col-xs-6 a::attr(href)").getall()
comic_date = Selector(html).css(".col-sm-6 .right::text").getall()
comic_id = Selector(html).css(".col-sm-6 .col-xs-6 a::attr(id)").getall()

cal = Calendar()

# timezone = Timezone()
# timezone.add('TZID', 'Asia/Shanghai')
# cal.add_component(timezone)

for name, url, udate, uid in zip(comic_name, comic_url, comic_date, comic_id):
    event = Event()
    try:
        time = datetime.strptime(udate, r"Set to Release %B %d, %Y")
    except:
        time = datetime.strptime(udate, r"Released %B %d, %Y")
    event.add("DTSTART", date(time.year, time.month, time.day))
    event.add("DTEND", date(time.year, time.month, time.day) + timedelta(days=1))
    event.add("SUMMARY", name)
    event.add("DESCRIPTION", url)
    event.add("UID", uid)

    alarm = Alarm()
    alarm.add('ACTION', 'DISPLAY')
    alarm['TRIGGER'] = 'P0DT9H0M0S'
    event.add_component(alarm)

    cal.add_component(event)

flag = False

with open('cal.ics', 'wb') as f:
        f.write(cal.to_ical())
