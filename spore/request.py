import json
import logging
import uuid
from typing import Union

import httpx

from .types import RequestError, RequestTimeout


class HttpRequest:
    def __init__(self, api_base, get_auth_token: Union[callable, str] = None):
        """
        - get_auth_token, could be a function or a string
            - If it is a function, will be called with three parameters:
                http_method: str, url: str, bodystring: str
            - If it is a string, it will be used as the auth token
            - If not specified, means no auth token is required.
        """
        self.api_base = api_base

        if isinstance(get_auth_token, str):
            self.get_auth_token = lambda _, __, ___: get_auth_token
        elif isinstance(get_auth_token, callable):
            self.get_auth_token = get_auth_token
        else:
            self.get_auth_token = lambda _, __, ___: None

        self.session = httpx.Client()

    def get(
        self, path, query_params: dict = None, headers=None, request_id=None, timeout=30
    ):
        url = self.api_base + path
        _token = self.get_auth_token("GET", path, "")
        _headers = _make_headers(_token, headers, request_id)

        try:
            logging.info(f"HTTP GET {url}")
            rsp = self.session.get(
                url, params=query_params, headers=_headers, timeout=timeout
            )
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.WriteTimeout) as e:
            raise RequestTimeout(None, str(e))
        except Exception as e:
            raise RequestError(1, str(e))

        return _parse_response(rsp)

    def post(
        self,
        path,
        query_params: dict = None,
        body: Union[dict, list] = None,
        headers: dict = None,
        request_id=None,
        timeout=30,
    ):
        url = self.api_base + path
        if body:
            bodystring = json.dumps(body)
        else:
            bodystring = {}
        _token = self.get_auth_token("POST", path, bodystring)
        _headers = _make_headers(_token, headers, request_id)

        try:
            logging.info(f"HTTP POST {url}")
            rsp = self.session.post(
                url,
                params=query_params,
                headers=_headers,
                data=bodystring,
                timeout=timeout,
            )
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.WriteTimeout) as e:
            raise RequestTimeout(None, str(e)) from None
        except Exception as e:
            raise RequestError(1, str(e)) from None

        return _parse_response(rsp)

    def put(
        self,
        path,
        query_params: dict = None,
        body: Union[dict, list] = None,
        headers: dict = None,
        request_id=None,
        timeout=30,
    ):
        url = self.api_base + path
        if body:
            bodystring = json.dumps(body)
        else:
            bodystring = {}
        _token = self.get_auth_token("PUT", path, bodystring)
        _headers = _make_headers(_token, headers, request_id)

        try:
            logging.info(f"HTTP PUT {url}")
            rsp = self.session.put(
                url,
                params=query_params,
                headers=_headers,
                data=bodystring,
                timeout=timeout,
            )
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.WriteTimeout) as e:
            raise RequestTimeout(None, str(e)) from None
        except Exception as e:
            raise RequestError(1, str(e)) from None

        return _parse_response(rsp)


def _make_headers(
    bearer_token: str = None, headers: dict = None, request_id: str = None
) -> dict:
    if not headers:
        headers = {}
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    if "Authorization" not in headers:
        if bearer_token:
            headers["Authorization"] = "Bearer " + bearer_token
    if "X-Request-ID" not in headers:
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
        err_id = body_json.get("error")
        err_msg = body_json.get("message")
        raise RequestError(err_id, err_msg) from None

    return body_json
