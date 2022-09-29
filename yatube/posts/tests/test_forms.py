from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="Test_User")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Тестовое описание группы",
        )

        cls.post = Post.objects.create(
            text="Тестовый текст поста",
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            "text": "Тестовый текст",
            "group": self.group.pk,
        }
        self.authorized_client.post(
            reverse("posts:create_post"), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text="Тестовый текст").exists())
        post = Post.objects.latest("id")
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.group_id, form_data["group"])

    def test_edit_post(self):
        """Проверка редактирования записи авторизированным клиентом."""
        post = Post.objects.create(
            text="Текст поста для редактирования",
            author=self.author,
            group=self.group,
        )
        form_data = {
            "text": "Отредактированный текст поста",
            "group": self.group.id,
        }
        response = self.authorized_client.post(
            reverse("posts:post_edit", args=[post.id]),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse("posts:post_detail", kwargs={"post_id": post.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        post = Post.objects.latest("id")
        self.assertTrue(post.text == form_data["text"])
        self.assertTrue(post.author == self.author)
        self.assertTrue(post.group_id == form_data["group"])
