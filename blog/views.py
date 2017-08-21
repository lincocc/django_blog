import uuid
from uuid import uuid4

import markdown as markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.urls import reverse

from .models import Post, Comment


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
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/detail.html', context)
