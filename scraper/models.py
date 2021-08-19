from django.db import models
from django.db.models.base import Model



# (url = , name = , followers = , last_updated_archive =)
class Publications(models.Model):
    url = models.CharField(unique=True, max_length=100)
    name = models.CharField(unique=True, max_length=100)
    followers = models.IntegerField(null=True)
    last_updated_archive = models.DateField(null=True) 

class Error_Log(models.Model):
    time = models.DateTimeField()
    reason = models.CharField(max_length=100)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)

# (medium_id, user_name = , full_name = , info = , follower_count = , following_count = , url = , member_since = , image_id = )
class Users(models.Model):
    medium_id = models.CharField(null=True, max_length=12)
    user_name = models.CharField(null=True, max_length=100)
    full_name = models.CharField(null=True, max_length=100)
    info = models.CharField(null=True,max_length=1000)
    following_count = models.IntegerField(null=True,)
    follower_count = models.IntegerField(null=True,)
    url = models.CharField(max_length=100, null=True,)
    member_since = models.DateField(null=True,)
    image_id = models.CharField(null=True, max_length=100)
    last_updated = models.DateTimeField(null=True)
    # tells if specific user should get scraped
    collect_user_info = models.BooleanField()

class Follower_Relations(models.Model):
    user1 = models.ForeignKey(Users, default=None, on_delete=models.SET_DEFAULT, null=True, related_name='user1_follower_relations_set')
    user2 = models.ForeignKey(Users, default=None, on_delete=models.SET_DEFAULT, null=True, related_name='user2_follower_relations_set')
    date = models.DateTimeField()
    
# (url = , publication = , date = , last_seen = )
class Archives(models.Model):
    url = models.CharField(max_length=100, unique=True)
    publication = models.ForeignKey(Publications, null=True, default=None,  on_delete=models.SET_DEFAULT)
    date = models.DateField(null=True)
    last_seen = models.DateTimeField(null=True)

# title = , read_time = , published = , last_seen = , publications = , archive = , user = , claps = ,
class Articles(models.Model):
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    read_time = models.IntegerField(null=True)
    published = models.DateField(null=True)
    last_seen = models.DateTimeField(null=True)
    publication = models.ForeignKey(Publications, null=True, default=None,  on_delete=models.SET_DEFAULT)
    archive = models.ForeignKey(Archives, null=True, default=None,  on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(Users, null=True, default=None,  on_delete=models.SET_DEFAULT)
    clap_count = models.IntegerField(null=True)
    voter_count = models.IntegerField(null=True)
    voter_scraped_date = models.DateTimeField(null=True)
    response_count = models.IntegerField(null=True)

# contains all image captions for each image of the article
class Figcaptions(models.Model):
    caption = models.CharField(max_length=1000)
    article = models.ForeignKey(to=Articles, on_delete=models.CASCADE)