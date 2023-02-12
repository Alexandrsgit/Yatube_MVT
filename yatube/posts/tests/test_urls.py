from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment
from http import HTTPStatus
from django.core.cache import cache


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        Group.objects.create(
            title='Тестовый заголовок',
            slug='1',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text='123',
            author=cls.user,
            post=cls.post,
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_homepage_guest(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_auth_user(self):
        """Страница / доступна авторизованному пользователю."""
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_slug_auth_user(self):
        """Страница /group/1/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/group/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_templates(self):
        """URL-адрес использует соответствующий шаблон."""
        template_url_name = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/1/',
            'posts/profile.html': '/profile/auth/',
            'posts/post_detail.html': '/posts/1/',
        }
        for template, address in template_url_name.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_post_create_guest(self):
        """Страница create перенаправляет не авторизованного
        пользователю."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_post_create_auth_user(self):
        """Страница create доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_not_found(self):
        """Проверка шаблона при ошибке 404."""
        response = self.guest_client.get('unexisting_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_post_edit_author(self):
        """Страница pose_edit доступна только автору."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_add_comment(self):
        """Внесение комментария только авторизованным пользователм."""
        response = self.authorized_client.get('/posts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
