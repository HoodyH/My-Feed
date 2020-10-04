import requests
from time import sleep
from my_feed import Source, Platforms

from my_feed.modules.post import PostModel, MediaModel
from my_feed.modules.types import PostType

HEADER = {'User-agent': 'bot'}


def channel_update(channel: Source):

    if not channel.is_time_to_update:
        return

    data = channel.update()

    for post in data:
        post: PostModel

        if post.type == PostType.TEXT:
            print(post.type, post.title)
            continue

        if post.type == PostType.EMBED:
            media = post.media[0]
            print(post.type, post.title, media.url)
            continue

        if post.type == PostType.NONE:
            print(post.type, post.title)
            continue

        if post.media and post.type == PostType.VIDEO:
            for media in post.media:
                media: MediaModel
                print(post.type, post.id, media.url)

        if post.media and post.type == PostType.IMAGE:
            for media in post.media:
                media: MediaModel

                res = requests.get(media.url, headers=HEADER)
                caption = f'{post.title}\nVia {post.url}'
                print(caption)

                if res.status_code == 200:
                    with open('img/%s.jpg' % media.id, 'wb') as f:
                        f.write(res.content)
                        f.close()

    channel.set_last_update_now()


if __name__ == '__main__':

    channel0 = Source(Platforms.REDDIT, 'youtubetitties')
    # channel1 = Source(Platforms.REDDIT, 'anime')
    # channel0 = Source(Platforms.INSTAGRAM, '4361837093')  # 7116996642
    # channel1 = Source(Platforms.INSTAGRAM, '4361837093')  # 'foodpoornitalia' 5925898947

    while True:
        channel_update(channel0)
        # channel_update(channel1)
        sleep(30)
