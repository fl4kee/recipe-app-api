"""
Тест для user API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Создает и возвращает нового пользователя"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Тест функционала пользователя для публичного использования"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Тестирует создание пользователя (успех)"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])  # создался пользователь
        self.assertTrue(user.check_password(payload['password']))  # пароль корректный
        self.assertNotIn('password', res.data)  # пароля нет в ответе пользователю

    def test_user_with_email_exists_error(self):
        """Проверяет что ошибка возвращается если уже существует пользователь с передаваемым email"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Проверяет что пароль не слишком короткий"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email'],
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Проверяет генерацию токена."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Проверят возвращение ошибки если креды невалидны."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com',  'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Проверяет возвращение ошибки если пароль не передан."""
        payload = {'email': 'test@example.com',  'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
