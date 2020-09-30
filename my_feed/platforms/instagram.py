import hashlib
import string
import random
import pprint

from instagram_web_api import (
    Client,
)

from my_feed.platforms import PlatformInterface
from my_feed.modules.post import PostModel
from my_feed.modules.types import PostType


class MyClient(Client):
    """
    cause of a lib bug in the web_api i have to redefine the _extract_rhx_gis
    """

    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()


class Instagram(PlatformInterface):

    def __init__(self):
        super().__init__()

        self.api = MyClient(auto_patch=True, drop_incompat_keys=False)

    @staticmethod
    def get_media_url(data):
        media = data.get('standard_resolution', {})
        return media.get('url')

    def post(self, user_id, last_update_id):
        """
        Get all the post from the user loaded
        Store them as a list of InstagramPost obj
        :return: InstagramPosts array
        """
        out = []

        items = self.api.user_feed(user_id)

        for item in items:
            node = item.get('node')

            caption = node.get('caption', {})
            text = ''
            if caption:
                text = caption.get('text', '')

            post = PostModel(
                post_id=node.get('shortcode'),
                title=text,
                created_at=node.get('created_time'),
                url=f'https://www.reddit.com{node.get("link")}'
            )

            post.type = PostType.IMAGE
            if node.get('is_video'):
                post.type = PostType.VIDEO

            """
            Check if is a post with multible elements
                - multi element post has media list inside carousel_media
                - if not the object media is no encapsulated
            """
            carousel = node.get('carousel_media')
            if carousel:
                for c in carousel:
                    media = c.get('videos' if post.type == PostType.VIDEO else 'images')
                    post.add_media(
                        media_id=None,
                        media_url=self.get_media_url(media)
                    )

            else:
                media = node.get('videos' if post.type == PostType.VIDEO else 'images')
                post.add_media(
                    media_id=None,
                    media_url=self.get_media_url(media)
                )

            out.append(post)

        return out

    def update(self, target, last_update_id):

        self._feed = self.post(target, last_update_id)
        self._update_last_post_id(last_update_id)

        return self._feed
