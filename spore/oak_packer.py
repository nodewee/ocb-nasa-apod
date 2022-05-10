from typing import Union

from .constants import INFO_CONTENT_TYPES


def pack_topic_props(
    title: str = None,
    description: str = None,
    price_asset_id: str = None,
    price_monthly_amount: str = None,
):
    """
    - price_asset_id, Allowed assets:
        - CNB (Chui niu bi), ID: `965e5c6e-434c-3fa9-b780-c50f43cd955c`
        - BTC (Bitcoin), ID: `c6d0c728-2624-429b-8e0d-d9d19b6592fa`
        - XIN (Mixin Network), ID: `c94ac88f-4671-3976-b60a-09064f1811e8`
        - PUSD (Pando USD), ID: `31d2ea9c-95eb-3355-b65b-ba096853bc18`
    """
    payload = {}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if price_asset_id is None or price_monthly_amount is None:
        pass
    else:
        payload["price"] = {"asset": price_asset_id, "m": price_monthly_amount}
    return payload


def pack_info(
    content_type: str,
    content_value: Union[str, dict],
    title: str = None,
    source: str = None,
    author: str = None,
):
    payload = {"content_type": content_type, "content_value": content_value}
    if title:
        payload["title"] = title
    if source:
        payload["source"] = source
    if author:
        payload["author"] = author
    return payload


def pack_text_content(text: str):
    return INFO_CONTENT_TYPES.TEXT, text


def pack_markdown_content(text: str):
    return INFO_CONTENT_TYPES.MARKDOWN, text


def pack_image_content(
    attachment_id: str,
    mime_type: str,
    width: int,
    height: int,
    size: int,
    thumbnail: str,
):
    """
    Arguments:
        "attachment_id": "read From POST /attachments",
        "mime_type": e.g. "image/jpeg",
        "width": e.g. 1024,
        "height": e.g. 1024,
        "size": e.g. 1024,
        "thumbnail": "base64 encoded",
    """
    payload = {
        "attachment_id": attachment_id,
        "mime_type": mime_type,
        "width": width,
        "height": height,
        "size": size,
        "thumbnail": thumbnail,
    }
    return INFO_CONTENT_TYPES.IMAGE, payload
