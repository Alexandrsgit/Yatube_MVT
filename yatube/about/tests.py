from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse


class aboutURLTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_about_author_and_tech_url_exist(self):
        """Проверка доступности адреса about/author и about/tech."""
        url_name = {
            'author': '/about/author/',
            'tech': '/about/tech/',
        }
        for resp, url in url_name.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_about_author_and_tech_template_exist(self):
        """Проверка доступности шаблонов about/author и about/tech."""
        url_name = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, url in url_name.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_about_page_have_template(self):
        """URL, генерируемые при помощи имён доступен."""
        template_pages_name = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
        }
        for template, reverse_name in template_pages_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
