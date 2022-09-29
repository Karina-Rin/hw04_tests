from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр неавторизованного клиента
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.get(username="Test_User")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = User.objects.create_user(username="author")

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(
            username="Test_User",
        )

        cls.group = Group.objects.create(
            id="10",
            title="Группа",
            slug="one_group",
            description="Проверка описания",
        )

        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=User.objects.get(username="Test_User"),
            group=Group.objects.get(title="Группа"),
        )

        cls.post_url = f"/posts/{cls.post.id}/"
        cls.post_edit_url = f"/posts/{cls.post.id}/edit/"
        cls.public_urls = (
            ("/", "index.html"),
            (f"/group/{cls.group.slug}/", "group_list.html"),
            (f"/profile/{cls.user.username}/", "profile.html"),
            (cls.post_url, "post_detail.html"),
        )
        cls.private_urls = (
            ("/create/", "create_post.html"),
            (cls.post_edit_url, "create_post.html"),
        )

    # Проверяем общедоступные страницы
    def test_public_pages(self):
        for data in self.public_urls:
            print(data[0])
            response = self.guest_client.get(data[0])
            self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем доступ для авторизованного пользователя и автора
    def test_private_pages(self):
        for data in self.private_urls:
            response = self.authorized_client.get(data[0])
            self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем статус 404 для авторизованного пользователя
    def test_task_list_url_redirect_anonymous(self):
        """Страница /unexisting_page/ не существует."""
        response = self.authorized_client.get("/unexisting_page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_list", kwargs={"slug": self.group.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": self.author}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ): "posts/post_detail.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": self.post.id}
            ): "posts/create_post.html",
            reverse("posts:create_post"): "posts/create_post.html",
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
