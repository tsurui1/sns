from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField('タグ名', max_length=255, unique=True)

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField('画像')
    caption = models.TextField('説明')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __str__(self):
        return f'{self.user}-{self.caption[:10]}'

class Chat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField('コメント')
    created_at = models.DateTimeField('作成日', default=timezone.now)

class Reply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField('コメント')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    target = models.ForeignKey(Chat, on_delete=models.CASCADE)

class DMChat(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    text = models.TextField('コメント')
    created_at = models.DateTimeField('作成日', default=timezone.now)