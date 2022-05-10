import logging
import uuid

import httpx

from .constants import API_BASE_URL, RequestError


def get(bearer_token, path: str, params: dict = None, append_headers: dict = None):
    url = API_BASE_URL + path
    headers = _prepare_request_headers(bearer_token, append_headers)
    print(f"HTTP GET {url}")
    rsp = httpx.get(url, params=params, headers=headers, timeout=5)
    return _parse_response(rsp)


def post(
    bearer_token,
    path: str,
    params: dict = None,
    append_headers: dict = None,
    body: any = None,
):
    url = API_BASE_URL + path
    headers = _prepare_request_headers(bearer_token, append_headers)
    print(f"HTTP POST {url}")
    rsp = httpx.post(url, params=params, headers=headers, json=body, timeout=10)
    return _parse_response(rsp)


def put(
    bearer_token,
    path: str,
    params: dict = None,
    append_headers: dict = None,
    body: any = None,
):
    url = API_BASE_URL + path
    headers = _prepare_request_headers(bearer_token, append_headers)
    print(f"HTTP PUT {url}")
    rsp = httpx.put(url, params=params, headers=headers, json=body, timeout=10)
    return _parse_response(rsp)


def _prepare_request_headers(
    bearer_token, headers: dict = None, request_id: str = None
) -> dict:
    if not headers:
        headers = {}
    headers["Content-Type"] = "application/json"
    if bearer_token:
        headers["Authorization"] = "Bearer " + bearer_token
    request_id = request_id if request_id else str(uuid.uuid4())
    headers["X-Request-Id"] = request_id
    return headers


def _parse_response(rsp: httpx.Response):
    try:
        body_json = rsp.json()
    except Exception:
        body_json = {}
    logging.debug(body_json)

    if rsp.status_code != 200:
        msg = body_json.get("message", "")
        raise RequestError(rsp.status_code, msg)

    if "error" in body_json:
        msg = body_json.get("error", {}).get("message", "")
        raise RequestError(rsp, body_json)

    return body_json
