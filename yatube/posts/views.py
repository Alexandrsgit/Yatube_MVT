from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Post, User, Comment, Follow
from .forms import PostForm, CommentForm
from utils import page_obj_func
from django.contrib.auth.decorators import login_required


def index(request):
    """Функция запроса главной страницы."""
    post_list = Post.objects.all()
    page_obj = page_obj_func(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Функция запроса страницы Group."""
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all()
    page_obj = page_obj_func(post_list, request)
    context = {
        'group': group, 'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Функция отображения профиля пользователя."""
    authuser = get_object_or_404(User, username=username)
    getcount = Post.objects.filter(author__username=username)
    post_list = Post.objects.filter(author=authuser)
    page_obj = page_obj_func(post_list, request)
    following = authuser.following.filter(
        user=request.user.id,
        author=authuser,
    ).exists
    context = {
        'authuser': authuser,
        'getcount': getcount,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Функция для отображения детальной информации поста."""
    postdetail = get_object_or_404(Post, id=post_id)
    post_all = Post.objects.all()
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post_id)
    context = {
        'postdetail': postdetail,
        'post_all': post_all,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Функция для создания поста."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


def post_edit(request, post_id):
    """Функция для редактирования поста."""
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save()
        post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': is_edit,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def add_comment(request, post_id):
    """Функция добавления комментария."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Странница постов избранных авторов."""
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = page_obj_func(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Подписка на автора."""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        if Follow.objects.filter(user=request.user, author=author):
            return redirect('posts:profile', username)
        else:
            Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора."""
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user).filter(author=author)
    follow.delete()
    return redirect('posts:profile', username)
