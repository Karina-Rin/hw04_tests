from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def index(request):

    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших зн. к меньшим)
    paginator = Paginator(Post.objects.all(), settings.PAGINATOR_DEFAULT_SIZE)
    page_number = request.GET.get("page")
    # Получаем набор записей для страницы с запрошенным номеро
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)

    # View-функция для страницы сообщества:


def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # Получаем набор записей для страницы с запрошенным номером
    paginator = Paginator(group.posts.all(), settings.PAGINATOR_DEFAULT_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


# Создать профил
def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    count = author.posts.count()
    paginator = Paginator(author.posts.all(), settings.PAGINATOR_DEFAULT_SIZE)
    # будем выгружать по 10 постов
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "count": count,
        "author": author,
    }
    return render(request, "posts/profile.html", context)


# Создать страницу поста
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    pub_date = post.pub_date
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all().count()
    context = {
        "post": post,
        "post_title": post_title,
        "author": author,
        "author_posts": author_posts,
        "pub_date": pub_date,
    }
    return render(request, "posts/post_detail.html", context)


# Создать новый пост, ф-я доступна только авторизованным пользователям
@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(f"/profile/{post.author}/", {"form": form})

    groups = Group.objects.all()
    context = {"form": form, "groups": groups}
    return render(request, "posts/create_post.html", context)


# Редактировать пост, ф-я доступна только авторизованным пользователям
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    groups = Group.objects.all()
    if request.user != post.author:
        return redirect("posts:post_detail", post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)
    context = {
        "form": form,
        "is_edit": True,
        "post": post,
        "is_edit": True,
        "groups": groups,
    }
    return render(request, "posts/create_post.html", context)
