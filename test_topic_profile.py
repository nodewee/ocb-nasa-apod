import json

from spore import oak, oak_packer

config = json.load(open("./data/config.json"))
topic_id = config["topic-id"]
topic_token = config["topic-token"]


def modify_topic_profile(title: str = None, description: str = None):
    props = oak_packer.pack_topic_props(title, description)
    r = oak.modify_topic_props(topic_token, topic_id, props)
    print(r)


def modify_topic_price(asset_id: str, monthly_amount: str):
    props = oak_packer.pack_topic_props(
        price_asset_id=asset_id, price_monthly_amount=monthly_amount
    )
    r = oak.modify_topic_props(topic_token, topic_id, props)
    print(r)


def read_topic():
    r = oak.read_topic(topic_token, topic_id)
    print(r)


# modify_topic_profile("NASA APOD", " NASA Astronomy Picture of the Day")
# modify_topic_price("965e5c6e-434c-3fa9-b780-c50f43cd955c", "1")
read_topic()
