import asyncio
import os
import aiohttp
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import UTC
import time
from django.utils import timezone
import requests
from .models import SocialDashboardData


class SocialDashboardHelper:
    """This class gets and re-arrange data from api.social-searcher.com/v2"""

    def get_tasks(self, session, keyword):
        """created as a placeholder for a future asynchronous loop"""
        tasks = []
        networks = ['instagram', "twitter",
                    "facebook", "youtube", "reddit", "flickr"]
        for net in networks:
            url = f'https://api.social-searcher.com/v2/search?q={keyword}&network={net}&limit=100&key={os.getenv("SOCIAL_MEDIA_SEARCH_API_KEY")}'
            tasks.append(asyncio.create_task(session.get(url, ssl=False)))
        return tasks

    async def get_data(self, keyword):
        """An asynchronous configuration for self.get_tasks() 
        returns a compiled list of data gotten from self.get_tasks """
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = self.get_tasks(session, keyword)
            responses = await asyncio.gather(*tasks)

            for response in responses:
                if response.status == 200:
                    results.append(await response.json())
                elif response.status == 503:
                    continue
                elif response.status == 403:
                    raise PermissionError('Api key limit reached')
                else:
                    continue
            return results

    def instagram_data(self, id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 \
               (KHTML, like Gecko) Mobile/15E148 Instagram 244.0.0.12.112 (iPhone12,1; iOS 15_5; en_US; en-US; scale=2.00;\
                828x1792; 383361019)',
        }
        url = f'https://i.instagram.com/api/v1/users/{id}/info/'
        try:
            response = requests.get(url, headers=headers).json()
            return {"username": response['user']['username'], "profile_picture": response['user']['profile_pic_url']}
        except:
            return {"username": 'N/A', "profile_picture": 'N/A'}

    def get_username(self, network, obj):
        if network == 'twitter' or network == "youtube" or network == 'reddit' or network == 'flickr':
            return obj.get('user', None).get('name', None)
        elif network == 'facebook':
            return obj.get('postid', None).split('/')[3]
        elif network == 'instagram':
            if self.instagram_data(obj.get('user', None).get('userid', None))['username'] != 'N/A':
                user_name = self.instagram_data(obj.get('user', None).get('userid', None))[
                    'username']
                return user_name
            else:
                return obj.get('user', None).get('userid', None)
        else:
            return "None"

    def profile_picture(self, social, obj=None):

        if social == 'twitter':
            return obj.get('user', None).get('image', None) if obj.get('user', None) is not None else \
                'https://static.vecteezy.com/system/resources/previews/002/534/045/original/social-media-twitter-logo-blue-isolated-free-vector.jpg'
        elif social == 'instagram':
            profile_picture = self.instagram_data(obj.get('user', None).get('userid', None))[
                'profile_picture']
            return profile_picture
        else:
            return "None"

    def get_engagements(self, socials, obj):

        if socials == "twitter":
            if obj.get('popularity', None):
                engagement = {"retweet": obj.get('popularity', None)[0]['count'],
                              "likes": obj.get('popularity', None)[1]['count']}
                return engagement
            else:
                return {"retweet": 0, "likes": 0}
        elif socials == 'instagram':
            if obj.get('popularity', None):
                engagement = {"comments": obj.get('popularity', None)[1]['count'],
                              "likes": obj.get('popularity', None)[0]['count']}
                return engagement
            else:
                return {"comment": 0, "likes": 0}
        else:
            return None

    def get_twitter_followers(self, social, obj):
        if social == 'twitter':
            try:
                followers = obj.get('user', None).get(
                    'influence').get('count', None)
                return followers
            except AttributeError:
                return None
        else:
            return None

    def format_date(self, obj):

        if obj is not None:
            date_object = parse(obj[:-6])
            return timezone.make_aware(date_object)
        else:
            return timezone.now()

    def gather_data(self, keyword):
        items = []
        check = []

        for item in asyncio.run(self.get_data(keyword)):
            for obj in item['posts']:
                try:
                    items.append({"network": obj['network'],
                                  "date_posted": self.format_date(obj.get('posted', None)),
                                  "postid": obj['postid'],
                                  "text_content": obj['text'],
                                  "media_content": obj.get('image', None),
                                  "language": obj.get('lang', None),
                                  "sentiment": obj['sentiment'],
                                  "post_url": obj['url'],
                                  "profile_name":  obj.get('user', None).get('name', None) if obj.get('user', None).get('name', None) else None,
                                  "profile_picture":  obj.get('user', None).get('image', None) if obj.get('user', None).get('image', None) else None,
                                  "twitter_followers": self.get_twitter_followers(obj.get('network', None), obj),
                                  "engagements": self.get_engagements(obj.get('network', None), obj)
                                  })
                except KeyError:
                    continue
        return items

    def save_data(self, keyword):
        """creates a new row if not in existence else update existing rows , where postid and newtork are 
        simultaneously equal"""
        data = self.gather_data(keyword)
        for item in data:
            obj, created = SocialDashboardData.objects.update_or_create(
                postid=item['postid'], network=item['network'], keyword=keyword,
                defaults={
                    'keyword': keyword,
                    'network': item['network'],
                    "date_posted": item["date_posted"],
                    "text_content": item["text_content"],
                    "media_content": item["media_content"],

                    "language": item["language"],
                    "sentiment": item["sentiment"],

                    "post_url": item["post_url"],
                    "profile_name": item["profile_name"],
                    "profile_picture": item.get('profile_picture', None),
                    "twitter_followers": item["twitter_followers"],
                    "engagements": item["engagements"]

                }
            )
