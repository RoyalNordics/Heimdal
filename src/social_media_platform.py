from abc import ABC, abstractmethod
from post import Post

class SocialMediaPlatform(ABC):
    @abstractmethod
    def post(self, post: Post):
        pass