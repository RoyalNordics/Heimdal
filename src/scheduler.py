from datetime import datetime
from typing import List
from post import Post

class Scheduler:
    def __init__(self):
        self.queue: List[Post] = []

    def add_post(self, post: Post):
        self.queue.append(post)
        self.queue.sort(key=lambda x: x.post_time)

    def get_ready_posts(self) -> List[Post]:
        now = datetime.now()
        ready_posts = [post for post in self.queue if post.post_time <= now]
        self.queue = [post for post in self.queue if post.post_time > now]
        return ready_posts