from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache


from posts.models import Post, Group


User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='1',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_index_contains_some_posts_on_page(self):
        """Првоеряем paginator на главной странице."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']),
                         Post.objects.count())

    def test_group_list_contains_some_posts_on_page(self):
        """Првоеряем paginator на странице групп."""
        response = self.authorized_client.get(reverse('posts:group_list',
                                              kwargs={'slug':
                                                      self.group.slug}))
        self.assertEqual(len(response.context['page_obj']),
                         Group.objects.count())

    def test_profile_contains_some_posts_on_page(self):
        """Првоеряем paginator на страинце профиля."""
        response = self.authorized_client.get(reverse('posts:profile',
                                              kwargs={'username':
                                                      self.user.username}))
        self.assertEqual(len(response.context['page_obj']),
                         User.objects.count())
