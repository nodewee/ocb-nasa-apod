""" Oak Topic Bot - NASA Astronomy Picture of the Day

    > Run once a day
"""
import json
from io import BytesIO, FileIO

import httpx

from google.translator import translater
from nasa.apod import get_day_image
from spore import oak
from spore.oak_packer import pack_image_content, pack_info

config = json.load(open("./data/config.json"))
topic_id = config["topic-id"]
topic_token = config["topic-token"]
nasa_api_key = config["nasa-api-key"]


def calc_image_props(fileio: FileIO):
    """return (width, height, image_format, thumbnail_blurhash)"""
    import blurhash
    import PIL.Image

    img = PIL.Image.open(fileio)
    width, height = img.size

    img.thumbnail((64, 64))
    tmp_file = BytesIO()
    img.save(tmp_file, format=img.format)
    thumbnail_blurhash = blurhash.encode(tmp_file, x_components=4, y_components=3)

    return (width, height, img.format, thumbnail_blurhash)


def download_file(url, fileio: FileIO):
    """ "return size"""
    headers = {}
    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    with httpx.stream("GET", url, follow_redirects=True) as response:
        total = int(response.headers["Content-Length"])
        for chunk in response.iter_bytes():
            fileio.write(chunk)

    return total


def main():
    print("get today's image...", flush=True)
    item = get_day_image(nasa_api_key)
    if not item:
        print("No image found for today")
        return

    media_type = item.get("media_type")
    if media_type != "image":
        print(f"Media type is {media_type}, not supported currently")
        return

    author = item.get("copyright")
    title = item.get("title")
    source = item.get("hdurl")
    img_url = item.get("url")
    explanation = item.get("explanation")
    pub_date = item.get("date")

    tmp_file = "./temp-image.tmp"

    print(f"Downloading {img_url}", flush=True)
    size = download_file(img_url, open(tmp_file, "wb"))

    print("Calculating image properties ...", flush=True)

    width, height, image_format, thumbnail = calc_image_props(open(tmp_file, "rb"))
    print(
        f"Image: {image_format}, {size} bytes, {width}x{height} px,\n\tthumbnail blurhash: {thumbnail}"
    )

    print("Translating description ...", flush=True)
    description = f"{title}.\n{explanation}"
    description_zh, _ = translater.translate(description, "en", "zh-CN")
    description_zh = "(机器翻译)" + description_zh + f"\n{pub_date}"

    print("Post image to topic, ...", flush=True)
    # create attachment
    r = oak.create_attachment(topic_token)
    attachment_id = r["data"]["attachment_id"]
    upload_url = r["data"]["upload_url"]

    # upload image(attachment)
    r = oak.upload_attachment(upload_url, open(tmp_file, "rb"))
    content_type, content_value = pack_image_content(
        attachment_id, f"image/{image_format}", width, height, size, thumbnail
    )

    # post info to topic
    info = pack_info(
        content_type, content_value, title=description_zh, source=source, author=author
    )
    r = oak.post_to_topic(topic_token, topic_id, [info])
    print(r)


main()
