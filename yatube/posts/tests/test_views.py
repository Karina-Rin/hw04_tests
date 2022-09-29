from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        cls.user = User.objects.create(
            username="Test_User",
        )

        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Проверка описания",
        )

        bilk_post: list = []
        for i in range(13):
            bilk_post.append(
                Post(
                    text=f"Тестовый текст",
                    group=cls.group,
                    author=cls.user,
                )
            )
        Post.objects.bulk_create(bilk_post)

        post_args = 1
        cls.index_url = ("posts:index", "posts/index.html", None)
        cls.group_url = (
            "posts:group_list",
            "posts/group_list.html",
            cls.group.slug,
        )
        cls.profile_url = (
            "posts:profile",
            "posts/profile.html",
            cls.user.username,
        )
        cls.post_url = (
            "posts:post_detail",
            "posts/post_detail.html",
            post_args,
        )
        cls.new_post_url = (
            "posts:create_post",
            "posts/create_post.html",
            None,
        )
        cls.edit_post_url = (
            "posts:post_edit",
            "posts/create_post.html",
            post_args,
        )
        cls.paginated_urls = (cls.index_url, cls.group_url, cls.profile_url)

    def setUp(self):
        # Создаем неавторизованный + авторизованый клиент
        self.guest_client = Client()
        self.user = User.objects.get(username="Test_User")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse(self.index_url[0]): self.index_url[1],
            reverse(
                self.group_url[0], kwargs={"slug": self.group_url[2]}
            ): self.group_url[1],
            reverse(
                self.profile_url[0], kwargs={"username": self.profile_url[2]}
            ): self.profile_url[1],
            reverse(
                self.post_url[0], kwargs={"post_id": self.post_url[2]}
            ): self.post_url[1],
            reverse(
                self.edit_post_url[0],
                kwargs={"post_id": self.edit_post_url[2]},
            ): self.edit_post_url[1],
            reverse(self.new_post_url[0]): self.new_post_url[1],
        }
        # Проверяем, что при обращении к name вызывается HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста страниц
    def test_index_page_show_correct_context(self):
        """index, group_list, profile сформированы с правильным контекстом."""
        pages_names = [
            reverse(self.index_url[0]),
            reverse(self.group_url[0], kwargs={"slug": self.group_url[2]}),
            reverse(
                self.profile_url[0], kwargs={"username": self.profile_url[2]}
            ),
        ]

        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template)
                first_object = response.context["page_obj"][0]
                task_author = first_object.author.username
                task_text = first_object.text
                task_group = first_object.group.title
                self.assertEqual(task_author, "Test_User")
                self.assertEqual(task_text, "Тестовый текст")
                self.assertEqual(task_group, "Тестовая группа")

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(self.post_url[0], args=[self.post_url[2]])
        )
        post = response.context["post"]
        self.assertEqual(post.pk, self.post_url[2])

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(self.edit_post_url[0], args=[self.edit_post_url[2]])
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(self.new_post_url[0]))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_urls_first_page_contains_10_records(self):
        """10 постов на страницу у index, group и profile"""
        pages_names = [
            reverse(self.index_url[0]),
            reverse(self.group_url[0], kwargs={"slug": self.group_url[2]}),
            reverse(
                self.profile_url[0], kwargs={"username": self.profile_url[2]}
            ),
        ]
        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template)
                self.assertEqual(len(response.context["page_obj"]), 10)

    def test_urls_second_page_contains_3_records(self):
        """3 поста на второй странице index, group и profile"""
        pages_names = [
            reverse(self.index_url[0]),
            reverse(self.group_url[0], kwargs={"slug": self.group_url[2]}),
            reverse(
                self.profile_url[0], kwargs={"username": self.profile_url[2]}
            ),
        ]
        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template + "?page=2")
                self.assertEqual(len(response.context["page_obj"]), 3)

    def test_post_in_index_group_profile_after_create(self):
        """Созданный пост появился на главной, в группе, в профиле автора."""
        reverse_page_names_post = {
            reverse(self.index_url[0]): self.group_url[2],
            reverse(
                self.group_url[0], kwargs={"slug": self.group_url[2]}
            ): self.group_url[2],
            reverse(
                self.profile_url[0], kwargs={"username": self.profile_url[2]}
            ): self.group_url[2],
        }
        for value, expected in reverse_page_names_post.items():
            response = self.authorized_client.get(value)
            for object in response.context["page_obj"]:
                post_group = object.group.slug
                with self.subTest(value=value):
                    self.assertEqual(post_group, expected)

    def test_post_not_in_foreign_group(self):
        """Созданного поста НЕТ в чужой группе"""
        Group.objects.create(
            title="группа_check",
            slug="test_slug_check",
            description="проверка описания_check",
        )
        response = self.authorized_client.get(
            reverse(self.group_url[0], kwargs={"slug": "test_slug_check"})
        )
        for object in response.context["page_obj"]:
            post_slug = object.group.slug
            self.assertNotEqual(post_slug, self.group.slug)
