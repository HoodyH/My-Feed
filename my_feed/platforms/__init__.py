from abc import ABC, abstractmethod
from typing import List
from my_feed.modules.post import PostModel


class PlatformInterface(ABC):

    def __init__(self):
        # ID of the last post get
        self._last_post_id = None

    @property
    def last_post_id(self):
        """
        The the last post Id
        This property must be get after the update
        :return: a slug ID
        """
        return self._last_post_id

    @abstractmethod
    def update(self, target, last_update_id) -> List[PostModel]:
        """
        Function that get the data from the platform api
        and set the last post_id
        :param target: the name of the channel
        :param last_update_id: the last post id known
        :return: a list of posts
        """
        pass
