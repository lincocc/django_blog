import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_modified = models.DateTimeField('last modified', auto_now=True)
    summary = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_posts'
        ordering = ['-pub_date']


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
        ordering = ['-pub_date']


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_tags'
        ordering = ['name']


@receiver(post_save, sender=Comment)
def handle_comment_post(sender, instance=None, created=False, **kwargs):
    print("post save:%s" % sender)
    print(kwargs)


@receiver(pre_save, sender=Comment)
def handle_comment_pre(sender, **kwargs):
    print("pre save:%s" % sender)
    print(kwargs)


# @receiver(request_started)
# def handle_request_started(sender, **kwargs):
#     print("request_started:%s" % sender)
#     print(kwargs)
#
#
# @receiver(request_finished)
# def handle_request_finished(sender, **kwargs):
#     print("request_finished:%s" % sender)
#     print(kwargs)
