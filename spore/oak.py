from io import FileIO
from typing import Union

from . import request


def read_topic(token, topic_id: str):
    path = f"/oth/topics/{topic_id}"
    return request.get(token, path)


def post_to_topic(token, topic_id: str, infos: list):
    path = f"/oth/topics/{topic_id}"
    body = {"infos": infos}
    return request.post(token, path, body=body)


def modify_topic_props(token, topic_id: str, props: dict):
    if not props:
        raise ValueError("props is empty")
    path = f"/oth/topics/{topic_id}"
    body = props
    return request.put(token, path, body=body)


def create_attachment(token):
    path = "/oth/attachments"
    return request.post(token, path)


def read_attachment(token, attachment_id: str):
    path = f"/oth/attachments/{attachment_id}"
    return request.get(token, path)


def upload_attachment(upload_url: str, file: Union[FileIO, bytes]):
    """use create_attachment() to get upload_url"""
    import httpx

    headers = {}
    headers["Content-Type"] = "application/octet-stream"
    headers["x-amz-acl"] = "public-read"

    return httpx.put(upload_url, data=file, headers=headers, timeout=120)
