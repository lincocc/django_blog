import uuid
from uuid import uuid4

import markdown as markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from blog.serializers import PostSerializer
from .models import Post, Comment, Tag
from .form import PostForm, RegisterForm


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


@csrf_exempt
def api_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def api_post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)
