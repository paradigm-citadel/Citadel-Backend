from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


User = get_user_model()


# При некоторых конфигурация проектов с silk, данный тест падает с ошибкой
# Поэтому мокаю настройки и убирают из них silk
mocked_installed_apps = list(settings.INSTALLED_APPS)
try:
    mocked_installed_apps.remove('silk')
except ValueError:
    pass

mocked_middleware = list(settings.MIDDLEWARE)
try:
    mocked_middleware.remove('silk.middleware.SilkyMiddleware')
except ValueError:
    pass


@override_settings(
    # Мокаю настройку урл, чтобы протестить резолвинг и работу тестовых вьюх
    ROOT_URLCONF='bulk_requests.tests.mocks.urls',
    INSTALLED_APPS=mocked_installed_apps,
    MIDDLEWARE=mocked_middleware,
)
class BulkGETTests(APITestCase):
    def test_bulk_get_api(self):
        self.client.force_authenticate(user=User.objects.create(email='someusername'))

        url = reverse('bulk-get')
        data = {
            'endpoints': [
                {
                    'url': '/some-api/?logic-query=tests',
                },
                {
                    'url': '/another-api/',
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'endpoints': [
                    {
                        'url': '/some-api/?logic-query=tests',
                        'http_code': status.HTTP_200_OK,
                        'response_body': {
                            'result': 'yes'
                        }
                    },
                    {
                        'url': '/another-api/',
                        'http_code': status.HTTP_200_OK,
                        'response_body': {
                            'result': 'hello'
                        }
                    }
                ]
            }
        )
