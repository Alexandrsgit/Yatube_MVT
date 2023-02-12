from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms


User = get_user_model()


class UsersPagesTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='TestAuthUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_pages_have_correct_template(self):
        """URL-адрес users использует соотвествующимй шаблон."""
        template_pages_name = {
            'users/signup.html': reverse('users:signup'),
            'users/login.html': reverse('users:login'),
            'users/logged_out.html': reverse('users:logout'),
            'users/password_reset_form.html': reverse('users:password_reset'),
            'users/password_reset_done.html': reverse('users:'
                                                      'password_reset_done'),
            'users/password_reset_complete.html':
            reverse('users:password_reset_complete'),
        }
        for template, reverse_name in template_pages_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_form_is_correct(self):
        """Проверка signup на корректность формы."""
        response = self.authorized_client.get(reverse('users:signup'))
        forms_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                forms_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(forms_field, expected)
