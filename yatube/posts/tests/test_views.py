from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from posts.models import Post, Group, Comment, Follow


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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
        small_gif = (
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            image=uploaded,
        )
        cls.comment = Comment.objects.create(
            text='Тестовый коммент',
            author=cls.user,
            post=cls.post,
        )
        cls.template_pages_name = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list',
                                             kwargs={'slug': cls.group.slug}),
            'posts/profile.html': reverse('posts:profile',
                                          kwargs={'username':
                                                  cls.user.username}),
            'posts/post_create.html': reverse('posts:post_create'),
            'posts/post_detail.html': reverse('posts:post_detail',
                                              kwargs={'post_id': cls.post.id}),
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user2 = User.objects.create_user(username='follower')
        self.follower_client = Client()
        self.follower_client.force_login(self.user2)
        self.user3 = User.objects.create_user(username='unfollower')
        self.unfollower_client = Client()
        self.unfollower_client.force_login(self.user3)

    def test_views_have_correct_template(self):
        """URL-адрес posts использует соотвествующимй шаблон."""
        for template, reverse_name in self.template_pages_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_views_post_edit_have_correct_template(self):
        """URL-адрес post_edit использует соотвествующимй шаблон."""
        response = self.authorized_client.get(reverse('posts:post_edit',
                                              kwargs={'post_id':
                                                      self.post.id}))
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_index_have_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0.username, self.user.username)
        self.assertEqual(post_image_0, self.post.image)

    def test_cash_index(self):
        """Тестирование кэша главной страницы."""
        till_del = self.authorized_client.get(reverse('posts:index')).content
        all_content = Post.objects.all()
        all_content.delete()
        after_del = self.authorized_client.get(reverse('posts:index')).content
        self.assertEqual(till_del, after_del)
        cache.clear()
        after_clr = self.authorized_client.get(reverse('posts:index')).content
        self.assertNotEqual(till_del, after_clr)

    def test_group_list_have_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list',
                                              kwargs={'slug':
                                                      self.group.slug}))
        self.assertEqual(response.context.get('group').title,
                         self.group.title)
        self.assertEqual(response.context.get('group').slug, self.group.slug)
        self.assertEqual(response.context.get('group').description,
                         self.group.description)
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0.username, self.user.username)
        self.assertEqual(post_image_0, self.post.image)

    def test_profile_have_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile',
                                                      kwargs={'username':
                                                              self.user.
                                                              username}))
        self.assertEqual(response.context.get('authuser').username,
                         self.user.username)
        self.assertEqual(response.context.get('getcount').count(),
                         self.post.author.posts.count())
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0.username, self.user.username)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_detail_have_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_detail',
                                              kwargs={'post_id':
                                                      self.post.id}))
        self.assertEqual(response.context.get('postdetail').id, self.post.id)
        first_object = response.context['post_all'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_id_0 = first_object.id
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0.username, self.user.username)
        self.assertEqual(post_id_0, self.post.id)
        self.assertEqual(post_image_0, self.post.image)

    def test_post_add_comment_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_detail',
                                              kwargs={'post_id':
                                                      self.post.id}))
        self.assertEqual(response.context.get('postdetail').id, self.post.id)
        first_object = response.context['comments'][0]
        post_comment_0 = first_object.text
        self.assertEqual(post_comment_0, self.comment.text)

    def test_post_edit_form_fields(self):
        """Проверка post_edit на корректность формы."""
        response = self.authorized_client.get(reverse('posts:post_edit',
                                              kwargs={'post_id':
                                                      self.post.id}))
        forms_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                forms_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(forms_field, expected)
        self.assertEqual(response.context.get('is_edit'), True)
        self.assertEqual(response.context.get('post').id, self.post.id)

    def test_follow_unfollow(self):
        """Проверяем работу подписки и отписки от автора."""
        self.follower_client.get(reverse('posts:profile_follow',
                                 kwargs={'username': self.user.username}))
        follow = Follow.objects.filter(user=self.user2, author=self.user)
        self.assertTrue(follow.exists())
        self.follower_client.get(reverse('posts:profile_unfollow',
                                 kwargs={'username': self.user.username}))
        unfollow = Follow.objects.filter(user=self.user2, author=self.user)
        self.assertFalse(unfollow.exists())

    def test_follow_user_have_follower_post(self):
        """Проверяем наличие поста у подписчика на автора и отсутствие поста
        у не подписчика."""
        self.follower_client.get(reverse('posts:profile_follow',
                                 kwargs={'username': self.user.username}))
        Follow.objects.filter(user=self.user2, author=self.user)
        response = self.follower_client.get(reverse('posts:follow_index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        self.assertEqual(post_text_0, self.post.text)
        response2 = self.unfollower_client.get(reverse('posts:follow_index'))
        self.assertNotEqual(response2.context, response.context)
