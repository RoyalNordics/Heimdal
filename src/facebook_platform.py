from social_media_platform import SocialMediaPlatform
from post import Post

class FacebookPlatform(SocialMediaPlatform):
    def post(self, post: Post):
        print(f"Posting to Facebook: {post.content}")