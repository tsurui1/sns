from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.ImageField('プロフィール画像', blank=True, null=True)
    profile = models.TextField('プロフィール', blank=True, null=True)
    follow = models.ManyToManyField('CustomUser', blank=True, related_name='follower')
    like = models.ManyToManyField('insta.Post', blank=True, related_name='like_user')
    bookmark = models.ManyToManyField('insta.Post', blank=True, related_name='bookmark_user')

    def __str__(self):
        return self.username