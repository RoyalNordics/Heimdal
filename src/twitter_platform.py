from social_media_platform import SocialMediaPlatform
from post import Post

class TwitterPlatform(SocialMediaPlatform):
    def post(self, post: Post):
        print(f"Posting to Twitter: {post.content}")