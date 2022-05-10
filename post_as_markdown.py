""" Oak Topic Bot - Astronomy Picture of the Day

    > Run once a day
"""
import json

from nasa.apod import get_day_image
from spore import oak
from spore.oak_packer import pack_info, pack_markdown_content

config = json.load(open("./data/config.json"))
topic_id = config["topic-id"]
topic_token = config["topic-token"]
nasa_api_key = config["nasa-api-key"]

from google.translator import translater


def main():
    print("get today's image", flush=True)
    item = get_day_image(nasa_api_key)
    if not item:
        print("No image found for today")
        return

    media_type = item.get("media_type")
    if media_type != "image":
        return  # ignore non-image

    author = item.get("copyright")
    title = item.get("title")
    hd_img_url = item.get("hdurl")
    img_url = item.get("url")
    explanation = item.get("explanation")
    pub_date = item.get("date")

    print("Translating content ...", flush=True)
    content = f"{title}.\n{explanation}"
    content_zh, _ = translater.translate(content, "en", "zh-CN")

    md = f"NASA Astronomy Picture of the Day {pub_date}\n\n"
    md += f"![]({img_url})\n \n[> 高清大图]({hd_img_url})\n\n"
    md += f"(机器翻译) {content_zh}\n\n"
    md += f"原文:\n> {content}\n\n"
    content_type, content_value = pack_markdown_content(md)

    # post info to topic
    info = pack_info(
        content_type, content_value, title=title, source=hd_img_url, author=author
    )
    r = oak.post_to_topic(topic_token, topic_id, [info])
    print(r)


main()
