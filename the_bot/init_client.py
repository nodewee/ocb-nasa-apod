import json

from spore.client import SporeClient

channel_config = json.load(open("../config/channel.json"))
channel_id = channel_config["channel-id"]
channel_token = channel_config["channel-token"]

nasa_config = json.load(open("../config/nasa.json"))
nasa_api_key = nasa_config["api-key"]


spore_client = SporeClient(channel_token)
