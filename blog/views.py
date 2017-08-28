import uuid

import markdown as markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from rest_framework import permissions, viewsets

from blog.serializers import PostSerializer, UserSerializer, CommentSerializer, TagSerializer
from permissions import IsUserOrReadOnly
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


class IndexView(ListView):
    queryset = Post.objects.order_by('-pub_date').all()
    paginate_by = 10
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        posts = context[self.context_object_name]
        posts.number = page_obj.number
        if paginator and page_obj:
            context.update({'page_range': get_page_range(page_obj.number, paginator)})
        return context


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


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post_uuid = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(self.model, pk=uuid.UUID(post_uuid))

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = context[self.context_object_name]
        post.content = markdown.markdown(post.content,
                                         extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        comments = post.comment_set.order_by('-pub_date').all()
        tags = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
        context.update({'comments': comments, 'tags': tags})
        return context

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        post_uuid = self.kwargs.get(self.pk_url_kwarg)
        post = self.get_object()
        if content:
            Comment.objects.create(content=content, user=request.user, post=post)
            return HttpResponseRedirect(reverse('blog:detail', args=(post_uuid,)))


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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by('id').all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
