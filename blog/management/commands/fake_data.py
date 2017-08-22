import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from blog.models import Comment, Post, Tag


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


class Command(BaseCommand):
    help = 'Import init data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        fake_data()
        self.stdout.write(self.style.SUCCESS('end import'))
