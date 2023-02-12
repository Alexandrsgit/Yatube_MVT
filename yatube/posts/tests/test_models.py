from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Group, Post


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='A' * 20,
            author=cls.user,
        )

    def test_posts_have_correct_objects_names(self):
        """Проверяем, что у Post корректно работает __str__."""
        expected_object_name_post = PostModelTest.post.text
        self.assertEqual(str(PostModelTest.post),
                         expected_object_name_post[:15])

    def test_groups_have_correct_objects_names(self):
        """Проверяем, что у Group корректно работает __str__."""
        expected_object_name_group = PostModelTest.group.title
        self.assertEqual(str(PostModelTest.group), expected_object_name_group)

    def test_verbose_name_post(self):
        """Проверяем verbose_name в Post."""
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.post._meta.get_field(field).verbose_name,
                    expected_value)

    def test_verbose_name_group(self):
        """Проверяем verbose_name в Group."""
        field_verboses = {
            'title': 'Название',
            'slug': 'Номер группы',
            'description': 'Описание',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.group._meta.get_field(field).verbose_name,
                    expected_value)

    def test_help_text_post(self):
        """Проверяем help_text для Post."""
        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Выбирите группу',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.post._meta.get_field(field).help_text,
                    expected_value)

    def test_help_text_group(self):
        """Проверяем help_text для Group."""
        field_help_text = {
            'title': 'Введите название группы',
            'description': 'Введите описание группы',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.group._meta.get_field(field).help_text,
                    expected_value)
