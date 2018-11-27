from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .utlils import *
from .froms import *


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(ObjectCreateMxn, View):
    form_model = PostForm
    template = 'blog/post_create.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(ObjectCreateMxn, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
