from datetime import datetime
from typing import List
from post import Post
from scheduler import Scheduler
from social_media_platform import SocialMediaPlatform

class SocialMediaManager:
    def __init__(self):
        self.scheduler = Scheduler()
        self.platforms: List[SocialMediaPlatform] = []

    def add_platform(self, platform: SocialMediaPlatform):
        self.platforms.append(platform)

    def schedule_post(self, content: str, post_time_str: str, platform_name: str):
        post_time = datetime.strptime(post_time_str, "%Y-%m-%d %H:%M:%S")
        post = Post(content, post_time, platform_name)
        self.scheduler.add_post(post)

    def run_scheduler(self):
        ready_posts = self.scheduler.get_ready_posts()
        for post in ready_posts:
            for platform in self.platforms:
                if platform.__class__.__name__.startswith(post.platform):
                    platform.post(post)