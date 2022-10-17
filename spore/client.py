from . import api, constants, request


class SporeClient:
    def __init__(self, auth_token: str) -> None:
        self._request = request.HttpRequest(constants.API_BASE_URL, auth_token)
        self.api = api.ApiInterface(self._request)
