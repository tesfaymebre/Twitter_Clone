from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Tweets(models.Model):
    user = models.ForeignKey(User, related_name="tweets",on_delete=models.DO_NOTHING)
    body = models.CharField(max_length= 2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweet_like" , blank=True)
    image = models.ImageField( blank=True,null= True, upload_to='posts/')
    tag = models.CharField( blank=True,null= True,max_length=30)
    def __str__(self):
        return (
            f"{self.user}"
        )
   
   
    def like_counter(self):
        return self.likes.count()

   

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE)
    follows = models.ManyToManyField( "self" ,
                                     symmetrical=False,
                                     blank=True,
                                     related_name="followed_by")
    date_modified= models.DateTimeField(User,auto_now=True)
    profile_image = models.ImageField( blank=True,null= True, upload_to='images/')
    def __str__(self):
        return self.user.username
    @property
    def get_photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return "/static/images/default.jpg"

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()

        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile, sender=User)
