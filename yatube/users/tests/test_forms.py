from posts.models import User
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse


class UsersCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_create_user(self):
        """Тестируем форму создания пользователя."""
        user_count = User.objects.count()
        form_data = {
            'first_name': 'Test_fn_1',
            'last_name': 'Test_ln_1',
            'username': 'test_username_1',
            'email': 'test1@mail.ru',
            'password1': 'Password_test_123',
            'password2': 'Password_test_123',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name='Test_fn_1',
                last_name='Test_ln_1',
                username='test_username_1',
                email='test1@mail.ru',
            ).exists()
        )
