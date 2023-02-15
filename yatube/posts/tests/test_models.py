from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Group, Post, Comment, Follow


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user2 = User.objects.create_user(username='user2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='A' * 20,
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text='Тестовый текст комментария',
            author=cls.user2,
        )
        cls.follow = Follow.objects.create(
            user=cls.user2,
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
            'image': 'Картинка',
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
            'image': 'Загрузите изображение',
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

    def test_vebose_name_comment(self):
        """Тестирование verbose_name для Comment."""
        field_verboses = {
            'text': 'Комментарий',
            'author': 'Автор',
            'post': 'Пост',
            'created': 'Дата комментария',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.comment._meta.get_field(field).verbose_name,
                    expected_value)

    def test_verbose_name_follow(self):
        """Тестирование verbose_name для Follow."""
        field_verbose = {
            'user': 'Пользователь',
            'author': 'Избранный автор',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.follow._meta.get_field(field).verbose_name,
                    expected_value)

    def test_help_text_comment(self):
        """Тестирование help_text для Comment."""
        field_help_text = {
            'text': 'Введите комментарий',
            'created': 'Укажите дату',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.comment._meta.get_field(field).help_text,
                    expected_value)

    def test_help_text_follow(self):
        """Тестирование help_text для Follow."""
        field_help_test = {
            'user': 'Укажите пользователя',
            'author': 'Укажите автора поста',
        }
        for field, expected_value in field_help_test.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostModelTest.follow._meta.get_field(field).help_text,
                    expected_value)
