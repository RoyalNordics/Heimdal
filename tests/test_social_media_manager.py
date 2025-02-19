import pytest
from datetime import datetime, timedelta
from social_media_manager import SocialMediaManager
from facebook_platform import FacebookPlatform
from twitter_platform import TwitterPlatform
from instagram_platform import InstagramPlatform

def test_schedule_and_post():
    # Create instances of social media platforms
    facebook = FacebookPlatform()
    twitter = TwitterPlatform()
    instagram = InstagramPlatform()

    # Create a social media manager
    manager = SocialMediaManager()

    # Add platforms to the manager
    manager.add_platform(facebook)
    manager.add_platform(twitter)
    manager.add_platform(instagram)

    # Schedule a post
    future_time = (datetime.now() + timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    manager.schedule_post("Test Post", future_time, "Facebook")

    # Wait for the post time
    import time
    time.sleep(2)

    # Run the scheduler to post scheduled posts
    manager.run_scheduler()

    # Since we are using print statements, we can't directly assert the output
    # In a real-world scenario, we would mock the platform's post method and assert calls