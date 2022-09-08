import os

# ========== INIT Environment
#   统一本地与服务器的时间戳
os.environ["TZ"] = "UTC+00:00"

from the_bot import init_client, nasa_apod, channel

# publish info as markdown
title, content, source = nasa_apod.prepare_markdown()
channel.publish_markdown(content, title, source)

# # publish info as image
# file_io, file_size, text_comment, source = nasa_apod.prepare_image()
# channel.publish_image(file_io, file_size, text_comment, source)

print("Done!")
