from django.test import (TestCase,
                         Client)
from rest_framework import status

from employees_department.models import (Employee,
                                         Department)


URL_PATH = 'http://127.0.0.1:8000/'


class UrlAddressTest(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_department_url_available_all_users(self):
        response = self.guest_client.get(
            URL_PATH + 'api/v1/department/',
           )
        self.assertEqual(response.status_code, status.HTTP_200_OK)



