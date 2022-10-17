from typing import Union

from .constants import INFO_CONTENT_TYPES


def pack_channel_props(
    title: str = None,
    description: str = None,
    price_per_info: str = None,
    avatar: str = None,
):
    payload = {}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if price_per_info is not None:
        payload["price_per_info"] = price_per_info
    if avatar is not None:
        payload["avatar"] = avatar
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


def pack_video_content(
    attachment_id: str,
    mime_type: str,
    size: int,
    width: int,
    height: int,
    duration: int,
    thumbnail: str = None,
    created_at: str = None,
):
    """
    Args:
        attachment_id: "Read From POST /attachments"
        mime_type: e.g. "video/mp4"
        thumbnail: "base64 encoded"
    """
    payload = {
        "attachment_id": attachment_id,
        "mime_type": mime_type,
        "width": width,
        "height": height,
        "size": size,
        "duration": duration,
        "thumbnail": thumbnail,
        "created_at": created_at,
    }
    return INFO_CONTENT_TYPES.VIDEO, payload
