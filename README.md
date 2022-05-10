# OTBot-NASA-APOD

Oak Topic Bot - NASA Astronomy Picture of the Day

## Usage

1. Clone or download the repository.
2. Move file `config-example.json` to `./data/config.json`, and fill your oak topic id, token, and API key.
3. Install dependencies.
    `pip3 install -r requirements.txt`

4. Run testing scripts,

- `test_topic_profile.py`, read or edit your oak topic profile.
- `test_post_text.py`, post an text info to your oak topic.
- `test_attachment.py`, create and upload an image attachment.

5. Run bot scripts,

- `post_as_markdown.py`, get image feed from NASA API, and post it as markdown message to your oak topic.
- `post_as_image.py`, get image feed from NASA API, and post it as image message to your oak topic.

## References

API used:

- [InfoWoods API](https://github.com/infowoods/docs/blob/main/api-zh.md)
- [NASA API](https://api.nasa.gov/)
- Google Translator

Contact me on Mixin Messenger: `37297553`

## LICENSE

[GNU General Public License v3.0](https://github.com/nodewee/otbot-nasa-apod/blob/main/LICENSE)
