from django.db import models
from uuid import uuid4

class SocialDashboardData(models.Model):
    id=models.UUIDField(default=uuid4, editable=False, primary_key=True)
    keyword = models.CharField(max_length=2000, null=True)
    postid = models.CharField(max_length=2000, null=True)
    network = models.CharField(max_length=2000, null=True)
    date_posted= models.DateTimeField(null=True)
    text_content=models.CharField(max_length=2000, null=True)
    media_content=models.CharField(max_length=2000, null=True)
    language =models.CharField(max_length=2000, default='others',null=True)
    sentiment =models.CharField(max_length=2000, null=True)
    post_url =models.URLField(max_length=2000,null=True)
    profile_name =models.CharField(max_length=2000, null=True)
    profile_picture =models.URLField(max_length=2000,null=True)
    twitter_followers =models.IntegerField(default=0,null=True)
    engagements=models.JSONField(default=dict , null= True)
    modified_at = models.DateTimeField(auto_now=True)
