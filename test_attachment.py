import json

from spore import oak

config = json.load(open("./data/config.json"))
topic_id = config["topic-id"]
topic_token = config["topic-token"]

# create attachment
r = oak.create_attachment(topic_token)
new_attachment = r["data"]
print(new_attachment)

# upload attachment
upload_url = new_attachment["upload_url"]
r = oak.upload_attachment(upload_url, open("./data/test.gif", "rb"))
print(r)
