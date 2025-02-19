from social_media_platform import SocialMediaPlatform
from post import Post

class InstagramPlatform(SocialMediaPlatform):
    def post(self, post: Post):
        print(f"Posting to Instagram: {post.content}")