from io import FileIO
import httpx

from .request import HttpRequest


class ApiInterface:
    def __init__(self, request: HttpRequest):
        self._request = request

    def user_hi(self, headers: dict = None):
        path = f"/users/hi"
        return self._request.get(path, headers=headers)

    def user_me_read_all(self, headers: dict = None):
        path = f"/users/me"
        return self._request.get(path, headers=headers)

    def user_me_read_settings(self, headers: dict = None):
        path = f"/users/me?settings="
        return self._request.get(path, headers=headers)

    def user_me_modify_settings(self, settings: dict, headers: dict = None):
        path = f"/users/me"
        body = {"settings": settings}
        return self._request.put(path, body=body, headers=headers)

    def user_me_wallets(self, headers: dict = None):
        path = f"/users/me?wallets"
        return self._request.get(path, headers=headers)

    def orders_list_goods(self, headers: dict = None):
        path = "/orders/goods"
        return self._request.get(path, headers=headers)

    def orders_create(self, app_name, goods_id, headers: dict = None):
        path = "/orders/create"
        body = {"app_name": app_name, "goods_id": goods_id}
        return self._request.post(path, body=body, headers=headers)

    def orders_payment(self, app_name, trace_id, headers: dict = None):
        path = "/orders/payment"
        body = {"app_name": app_name, "mm_trace_id": trace_id}
        return self._request.post(path, body=body, headers=headers)

    def channels_list(self, headers: dict = None):
        path = f"/channels"
        return self._request.get(path, headers=headers)

    def channels_get_fees(
        self, channel_id: str = None, info_type: str = None, headers: dict = None
    ):
        path = f"/channels/fees?create"
        if channel_id:
            path += f"&channel_id={channel_id}"
        if info_type:
            path += f"&info_type={info_type}"
        return self._request.get(path, headers=headers)

    def channels_parse_uri(self, uri: str, headers: dict = None):
        path = f"/channels/parse"
        body = {"uri": uri}
        return self._request.post(path, body=body, headers=headers)

    def channels_search_channel(
        self, text: str, limit: int = None, headers: dict = None
    ):
        path = f"/channels/search"
        body = {"source": "channel", "text": text}
        if limit:
            body["limit"] = limit
        return self._request.post(path, body=body, headers=headers)

    def channels_search_weibo(self, uid_or_name: str, headers: dict = None):
        path = f"/channels/search"
        body = {"source": "weibo", "text": uid_or_name}
        return self._request.post(path, body=body, headers=headers)

    def channels_search_twitter(self, display_name: str, headers: dict = None):
        path = f"/channels/search"
        body = {"source": "twitter", "text": display_name}
        return self._request.post(path, body=body, headers=headers)

    def channels_read(self, channel_id: str, headers: dict = None):
        path = f"/channels/{channel_id}"
        return self._request.get(path, headers=headers)

    def channels_create(self, headers: dict = None):
        path = f"/channels"
        return self._request.post(path, headers=headers)

    def channels_publish_infos(
        self, channel_id: str, infos: list, headers: dict = None, timeout=30
    ):
        path = f"/channels/{channel_id}/infos"
        body = {"infos": infos}
        return self._request.post(path, body=body, headers=headers, timeout=timeout)

    def channels_modify(self, channel_id: str, props: dict, headers: dict = None):
        """
        Args:
            - props, use oak_packer.pack_channel_props() to make it
        """
        if not props:
            raise ValueError("props is empty")
        path = f"/channels/{channel_id}"
        body = props
        return self._request.put(path, body=body, headers=headers)

    def attachments_create(self, headers: dict = None):
        path = "/attachments"
        return self._request.post(path, headers=headers)

    def attachments_read(self, attachment_id: str, headers: dict = None):
        path = f"/attachments/{attachment_id}"
        return self._request.get(path, headers=headers)

    def attachments_upload(self, upload_url: str, file_io: FileIO, timeout: int = 120):
        """
        - upload_url, use attachment_create() to get

        Directly upload file to upload_url(AWS S3 URL from Mixin Messenger)
        """
        headers = {}
        headers["Content-Type"] = "application/octet-stream"
        headers["x-amz-acl"] = "public-read"
        # headers["Content-Length"] = str(len(file_data))

        params = {
            "url": upload_url,
            "data": file_io,
            "headers": headers,
            "timeout": timeout,
        }

        return httpx.put(**params)

    def subscriptions_subscribe(
        self,
        channel_id: str = None,
        channel_uri: str = None,
        headers: dict = None,
    ):
        """Subscribe a channel"""
        path = "/subscriptions"
        payload = {}
        if channel_id:
            payload["channel_id"] = channel_id
        if channel_uri:
            payload["channel_uri"] = channel_uri
        return self._request.post(path, body=payload, headers=headers)

    def subscriptions_unsubscribe(
        self,
        channel_id: str = None,
        channel_uri: str = None,
        headers: dict = None,
    ):
        """Unsubscribe a channel"""
        path = "/subscriptions"
        payload = {}
        if channel_id:
            payload["channel_id"] = channel_id
        if channel_uri:
            payload["channel_uri"] = channel_uri
        return self._request.delete(path, body=payload, headers=headers)

    def subscriptions_bulk_subscribe(
        self,
        channel_ids: list = None,
        channel_uris: list = None,
        collection_ids: list = None,
        headers: dict = None,
    ):
        """Bulk Subscribe channels"""
        path = "/subscriptions/assemble"
        payload = {"action": "bulk_subscribe"}
        if channel_ids:
            payload["channel_ids"] = channel_ids
        if channel_uris:
            payload["channel_uris"] = channel_uris
        if collection_ids:
            payload["collection_ids"] = collection_ids
        return self._request.post(path, body=payload, headers=headers)

    def subscriptions_bulk_unsubscribe(
        self,
        channel_ids: list = None,
        channel_uris: list = None,
        collection_ids: list = None,
        headers: dict = None,
    ):
        """Bulk Unsubscribe channels"""
        path = "/subscriptions/assemble"
        payload = {"action": "bulk_unsubscribe"}
        if channel_ids:
            payload["channel_ids"] = channel_ids
        if channel_uris:
            payload["channel_uris"] = channel_uris
        if collection_ids:
            payload["collection_ids"] = collection_ids
        return self._request.post(path, body=payload, headers=headers)

    def subscriptions_list_enabled(self, headers: dict = None):
        """List user's subscriptions"""
        path = f"/subscriptions?enabled=true"
        return self._request.get(path, headers=headers)

    def data_read(self, table: str, params: dict, headers: dict = None):
        path = f"/data/{table}"
        return self._request.get(path, query_params=params, headers=headers)

    def data_write(self, table: str, payload, headers: dict = None):
        path = f"/data/{table}"
        return self._request.post(path, body=payload, headers=headers)
