import json

from spore import oak, oak_packer

config = json.load(open("./data/config.json"))
topic_id = config["topic-id"]
topic_token = config["topic-token"]

info = oak_packer.pack_info(*oak_packer.pack_text_content("Hello World"))
r = oak.post_to_topic(topic_token, topic_id, [info])
print(r)
