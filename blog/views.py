import uuid

import markdown as markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.serializers import PostSerializer
from .form import PostForm, RegisterForm
from .models import Post, Comment, Tag


def index(request):
    # post_list = get_list_or_404(Post)
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'page_range': get_page_range(posts.number, paginator)}
    return render(request, 'blog/index.html', context)


def get_page_range(current_page, paginator):
    ON_EACH_SIDE = 3
    ON_ENDS = 2
    num_pages = paginator.num_pages
    if num_pages <= 10:
        page_range = paginator.page_range
    else:
        page_range = []
        if current_page > ON_EACH_SIDE + ON_ENDS + 1:
            page_range.extend(range(1, ON_ENDS + 1))
            page_range.append(None)
            page_range.extend(range(current_page - ON_EACH_SIDE, current_page + 1))
        else:
            page_range.extend(range(1, current_page + 1))

        if current_page < num_pages - ON_EACH_SIDE - ON_ENDS:
            page_range.extend(range(current_page + 1, current_page + ON_EACH_SIDE + 1))
            page_range.append(None)
            page_range.extend(range(num_pages - ON_ENDS + 1, num_pages + 1))
        else:
            page_range.extend(range(current_page + 1, num_pages + 1))

    return page_range


def detail(request, post_id):
    content = request.POST.get('content')

    post = Post.objects.get(pk=uuid.UUID(post_id))
    if content:
        Comment.objects.create(content=content, user=request.user, post=post)
        return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))
    comments = post.comment_set.order_by('-pub_date').all()
    # post.content = markdown2.markdown(text=post.content)
    post.content = markdown.markdown(post.content,
                                     extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
    tags = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    context = {'post': post, 'comments': comments, 'tags': tags}
    return render(request, 'blog/detail.html', context)


@login_required(login_url='blog_auth:login')
def edit(request, post_id=None):
    post = Post.objects.get(pk=uuid.UUID(post_id))

    # title = request.POST.get('title')
    # summary = request.POST.get('summary')
    # content = request.POST.get('content')
    # if title and summary and content:
    #     post.title = title
    #     post.summary = summary
    #     post.content = content
    #     post.save()
    #     return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editor.html', {'post': post, 'form': form})


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blog:index'))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                User.objects.get(email=email)
                form.add_error(None, {"email": "email exist"})
            except User.DoesNotExist:
                User.objects.create_user(username=username, email=email, password=password)
                return HttpResponseRedirect(reverse('blog_auth:login'))

    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
