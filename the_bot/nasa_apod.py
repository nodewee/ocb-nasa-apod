from google.translator import translater
from nasa.apod import get_day_image

from .init_client import nasa_api_key


def request_today_image():
    """return data, source"""
    print("get today's astronomy picture ...", flush=True)
    data = get_day_image(nasa_api_key)
    if not data:
        raise Exception("No image found for today")

    media_type = data.get("media_type")
    if media_type != "image":
        raise Exception(f"Not supprot media type: {media_type}")

    # pack source url
    date = data["date"]
    short_date = date.replace("-", "")[2:]
    source = f"https://apod.nasa.gov/apod/ap{short_date}.html"

    return data, source


def prepare_markdown():
    """return title, content, source"""
    item, source = request_today_image()

    author = item.get("copyright")
    title = item.get("title")
    hd_img_url = item.get("hdurl")
    img_url = item.get("url")
    explanation = item.get("explanation")
    pub_date = item.get("date")

    print("Translating content ...", flush=True)
    content = f"{title}.\n{explanation}"
    content_zh, _ = translater.translate(content, "en", "zh-CN")

    post_title = f"NASA 天文学图片 {pub_date}"
    post_content = ""
    post_content += f"![]({img_url})\n \n[🔗 高清大图]({hd_img_url})\n\n"
    post_content += f"Image Credit: {author}\n\n"
    post_content += f"(机器翻译) {content_zh}\n\n"
    post_content += f"原文:\n> {content}\n\n"

    return post_title, post_content, source


def prepare_image():
    """return file_io, file_size, text_comment, source"""
    item, source = request_today_image()

    author = item.get("copyright")
    title = item.get("title")
    hd_img_url = item.get("hdurl")
    img_url = item.get("url")
    explanation = item.get("explanation")
    pub_date = item.get("date")

    file_name, size = download_file(hd_img_url)

    print("Translating description ...", flush=True)
    description = f"{title}.\n{explanation}"
    # description_zh, _ = translater.translate(description, "en", "zh-CN")
    # description_zh = "(机器翻译)" + description_zh + f"\n{pub_date}"

    text_comment = f"Image Credit: {author}\n\n{description}"

    file_io = open(file_name, "rb")

    return file_io, size, text_comment, source


def download_file(url):
    """return file_name, size"""
    from urllib.parse import urlparse

    import httpx

    print("Downloading image ...", flush=True)

    file_name = "image.tmp"
    file_io = open(file_name, "wb")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Host": urlparse(url).netloc,
    }
    with httpx.stream("GET", url, follow_redirects=True) as response:
        total = int(response.headers["Content-Length"])
        for chunk in response.iter_bytes():
            file_io.write(chunk)
        file_io.flush()

    return file_name, total
