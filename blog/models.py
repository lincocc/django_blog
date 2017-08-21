import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    summary = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_posts'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'blog_comments'
