"""Image of the day
    https://www.nasa.gov/multimedia/imagegallery/iotd.html
"""
import calendar
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen


def parse_edt(est_str):
    """
    - est_str, e.g. Fri, 29 Apr 2022 09:07 EDT

    Return: (year:int, month:int, day:int)
    """

    _, d, m_abbr, y, hm, _ = est_str.split()
    m = list(calendar.month_abbr).index(m_abbr)
    return int(y), m, int(d)


def get_today_image():
    print("Fetching today's image from NASA ...", flush=True)
    url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"
    response = urlopen(url)
    content = response.read().decode("utf-8")

    root = ET.fromstring(content)

    today = time.gmtime()
    channel = root.find("channel")
    today_item = None
    for item in channel.iter("item"):
        title = item.find("title").text
        source = item.find("link").text
        description = item.find("description").text
        pub_date = item.find("pubDate").text
        year, month, day = parse_edt(pub_date)
        enclosure = item.find("enclosure")
        # if year == today.tm_year and month == today.tm_mon and day == today.tm_mday:
        today_item = {
            "title": title,
            "source": source,
            "img_url": enclosure.attrib["url"],
            "description": description,
            "pub_date": pub_date,
        }
        break
    return today_item
