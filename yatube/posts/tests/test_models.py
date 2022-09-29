from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
        )

    def test_models_post_have_correct_object_names(self):
        """Проверяем, что корректно работает __str__ у post."""
        self.assertEqual(self.post.text[:15], str(self.post))

    def test_models__group_have_correct_object_names(self):
        """Проверяем, что корректно работает __str__ у group."""
        self.assertEqual(self.group.title, str(self.group))

    # Проверка заполнения verbose_name в модели Post
    def test_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            "text": "Текст поста",
            "pub_date": "Дата публикации",
            "group": "Группа",
            "author": "Автор",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    # Проверка заполнения help_text в модели Post
    def test_help_text(self):
        field_help_texts = {
            "text": "Введите текст поста",
            "group": "Группа, к которой будет относиться пост",
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                error_name = f"Поле {value} ожидало значение {expected}"
                help_text = self.post._meta.get_field(value).help_text
                self.assertEqual(
                    help_text,
                    expected,
                    error_name,
                )
