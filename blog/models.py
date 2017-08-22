import random
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_tags'


def fake_data():
    User.objects.create_superuser(username='admin', email='admin@example.com', password='password123')
    user = User.objects.create_user(username='cc', email='cc@example.com', password='password123')
    users = [User.objects.create_user(username="user %s" % i, email="user%s@example.com" % i, password='password123')
             for i in range(0, 20)]
    users.append(user)

    def random_user():
        return users[random.randint(0, len(users) - 1)]

    def random_tags():
        return random.sample(tags, random.randint(1, 5))

    tags = [Tag.objects.create(name="tag %s" % i) for i in range(0, 20)]
    posts = []
    for i in range(0, 100):
        post = Post.objects.create(title="title %s" % i, summary="summary %s" % i, content="content %s" % i,
                                   user=random_user())
        post.tag_set.add(*random_tags())
        posts.append(post)

    def random_post():
        return posts[random.randint(0, len(posts) - 1)]

    [Comment.objects.create(content="content %s" % i, user=random_user(), post=random_post()) for i in
     range(0, 200)]
