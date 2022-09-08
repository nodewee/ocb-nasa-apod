""" Astronomy Picture of the Day
    https://apod.nasa.gov/apod/astropix.html
"""

import httpx


def get_day_image(api_key: str, date: str = None):
    """
    Args:
    - date: str, "YYYY-MM-DD"

    Return: data:dict
    """
    if not date:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    else:
        url = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={api_key}"
    r = httpx.get(url, timeout=60)

    data = r.json()
    return data
