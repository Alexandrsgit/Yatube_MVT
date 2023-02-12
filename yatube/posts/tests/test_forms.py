from posts.models import Post
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django import forms
from http import HTTPStatus
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


from django.contrib.auth import get_user_model


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Тестируем форму создания поста."""
        post_count = Post.objects.count()
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
        form_data = {
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                image='posts/small.gif'
            ).exists()
        )

    def test_create_post_guest(self):
        """Тестируем форму создания поста."""
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_form_fields(self):
        """Проверка post_create на корректность формы."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        forms_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                forms_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(forms_field, expected)

    def test_edit_from_fields(self):
        """Проверка post_edit на корректность формы."""
        response = self.authorized_client.get(reverse('posts:post_edit',
                                              kwargs=({'post_id':
                                                      self.post.id})))
        forms_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                forms_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(forms_field, expected)
