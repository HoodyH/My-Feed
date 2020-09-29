from enum import Enum
from datetime import datetime, timedelta

from my_feed.platforms.reddit import Reddit


class Platforms(Enum):
    REDDIT = Reddit
    INSTAGRAM = None


class Channel:

    def __init__(self, platform: Platforms, target: str):

        # in case of a non existing channel set as disabled, so it will not update
        self.is_enabled = True

        # The platform update type (reddit, instagram, etc)
        self.platform = platform
        self.updater = platform.value  # the updater Class

        # initialize last update with an old time
        self.last_update: datetime = datetime.now() - timedelta(hours=5)

        # update the data every minutes interval
        self.update_interval: int = 30

        # how to identify the last update, to not send again the same data
        # this value can be a string, slug, or int based on the platform that you are using
        self.last_update_id = None

        # the channel specification, this must match che update requirements in the platform api
        self.target: str = target

        # the exact time when the update start, to save it later
        self.updated_time = None

    @property
    def is_time_to_update(self):
        if datetime.now() - self.last_update > timedelta(minutes=self.update_interval) and self.is_enabled:
            return True
        return False

    def update(self):
        updater = self.updater()  # create the class
        out = updater.update(self.target, self.last_update_id)
        self.updated_time = datetime.now()
        return out

    def set_last_update_now(self):
        # update the last id
        self.last_update_id = self.updater.last_post_id
        self.last_update = self.updated_time
