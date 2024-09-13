import logging
from django.test import TestCase, Client  # Импортируем TestCase
from django.contrib.auth.models import User
import requests_mock

# Создание логгера
logger = logging.getLogger('tracker')


class AuthenticationTests(TestCase):

    def setUp(self):
        """ Инициализация клиента и пользователя """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login(self):
        """ Тестирование входа пользователя """
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)
        logger.info("Тест аутентификации: Вход прошёл успешно.")

    def test_logout(self):
        """ Тестирование выхода пользователя """
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302)
        logger.info("Тест аутентификации: Выход прошёл успешно.")


class APITests(TestCase):

    @requests_mock.Mocker()
    def test_get_aircraft_data(self, mock_request):
        """ Тестирование получения данных с API """
        mock_data = {
            "states": [
                ["abc123", None, "Country", None, None, 25.3134, 58.3134, None, None, None, None, None, None, None]
            ]
        }
        mock_request.get('https://opensky-network.org/api/states/all', json=mock_data)

        from .views import get_aircraft_data
        aircraft_data = get_aircraft_data()

        self.assertEqual(len(aircraft_data), 1)
        logger.info("Тест работы с API: Имитация запросов к API прошла успешно.")
