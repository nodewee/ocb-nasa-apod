from io import BytesIO, FileIO

from spore import oak_packer

from .init_client import channel_id, spore_client


def upload_image(image_file: str):
    """return view_url"""
    print("upload image attachment ...", flush=True)

    # create attachment
    r = spore_client.api.attachments_create()
    # attachment_id = r["data"]["attachment_id"]
    upload_url = r["data"]["upload_url"]
    view_url = r["data"]["view_url"]

    # upload image data to attachment
    r = spore_client.api.attachments_upload(upload_url, open(image_file, "rb"))
    print(r)

    return view_url


def publish_markdown(content: str, title: str = None, source: str = None):
    print("Publish markdown to channel ...", flush=True)
    content_type, content_value = oak_packer.pack_markdown_content(content)
    # post info to channel
    info = oak_packer.pack_info(content_type, content_value, title, source)
    r = spore_client.api.channels_publish_infos(channel_id, [info])
    print(r)


def publish_image(image_file_io, file_size, text_comment, source):
    print("Publish image to channel:", flush=True)
    # create attachment
    print("creating attachment ...")
    r = spore_client.api.attachments_create()
    attachment_id = r["data"]["attachment_id"]
    upload_url = r["data"]["upload_url"]

    print("uploading image attachment ...", flush=True)
    spore_client.api.attachments_upload(upload_url, image_file_io)

    width, height, image_format, thumbnail = calc_image_props(image_file_io)
    # print(
    #     f"Image: {image_format}, {file_size} bytes, {width}x{height} px,\n\tthumbnail blurhash: {thumbnail}"
    # )

    content_type, content_value = oak_packer.pack_image_content(
        attachment_id, f"image/{image_format}", width, height, file_size, thumbnail
    )

    # post info to topic
    info = oak_packer.pack_info(
        content_type, content_value, title=text_comment, source=source
    )
    print("posting info ...")
    r = spore_client.api.channels_publish_infos(channel_id, [info])
    print(r)


def calc_image_props(file_io: FileIO):
    """return (width, height, image_format, thumbnail_blurhash)"""
    import blurhash
    import PIL.Image

    print("calculating image properties ...", flush=True)

    img = PIL.Image.open(file_io)
    width, height = img.size

    img.thumbnail((64, 64))
    tmp_file = BytesIO()
    img.save(tmp_file, format=img.format)
    thumbnail_blurhash = blurhash.encode(tmp_file, x_components=4, y_components=3)

    return (width, height, img.format, thumbnail_blurhash)
