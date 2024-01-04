from django.test import (TestCase,
                         Client)
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from employees_department.models import (Employee,
                                         Department)


URL_PATH = 'http://127.0.0.1:8000/'


class UrlAddressTest(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
            )
        self.department = Department.objects.create(
            name='УНДО',
        )
        self.employee = Employee.objects.create(
            fio='Шумилов Александр Владимирович',
            foto=SimpleUploadedFile(name='test_image.jpg',
                                    content=open(
                                        'uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg',
                                        'rb').read(),
                                    content_type='image/jpeg'),
            position=True,
            salary=200000,
            age=25,
            department=self.department,
        )
        self.department.general = self.employee
        self.department.save()
        self.employee.save()

    def test_department_url_available_all_users(self):
        response = self.guest_client.get(
            URL_PATH + 'api/v1/department/',
           )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Нет доступа к странице.'
        )

    def test_department_url_access_all_users_for_specific_page(self):
        response = self.guest_client.get(
            URL_PATH + f'api/v1/department/{self.department.id}/'
           )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Нет доступа к странице.'
        )

    def test_no_access_for_unauthorized_user(self):
        response = self.guest_client.get(
            URL_PATH + 'api/v1/employee/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            'Есть доступ или иная ошибка.'
        )

    def test_no_access_for_unauthorized_user_for_specific_page(self):
        response = self.guest_client.get(
            URL_PATH + f'api/v1/employee/{self.employee.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            'Есть доступ или иная ошибка.'
        )

    def test_access_for_authorized_user(self):
        self.guest_client.login(
            username='admin',
            password='admin'
        )
        response = self.guest_client.get(
            URL_PATH + 'api/v1/employee/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Ошибка доступа к странице.'
        )

    def test_access_for_authorized_user_for_specific_page(self):
        self.guest_client.login(
            username='admin',
            password='admin'
        )
        response = self.guest_client.get(
            URL_PATH + f'api/v1/employee/{self.employee.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Ошибка доступа к странице.'
        )

    def tearDown(self):
        super().tearDown()



