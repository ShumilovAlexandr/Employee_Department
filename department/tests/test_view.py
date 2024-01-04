from django.test import (Client,
                         TestCase)
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import (Count,
                              Sum)

from employees_department.models import (Employee,
                                         Department)

OBJECT_ON_PAGE = 5
URL_PATH = 'http://127.0.0.1:8000/'


class EmployeeDepartmentViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_employee_being_create(self):
        department = Department.objects.create(name='УНДО')
        response = self.client.post(path=URL_PATH + 'api/v1/employee/',
                                    data={
                                        'fio': 'Шумилов Александр '
                                               'Владимирович',
                                        'foto': SimpleUploadedFile(name='test_image.jpg',
                                                                   content=open('uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg', 'rb').read(),
                                                                   content_type='image/jpeg'),
                                        'position': Employee.Position.GENERAL_MANAGER,
                                        'salary': 250000,
                                        'age': 28,
                                        'department': department.id
                                        }
                                    )
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_department_being_create(self):
        employee_data = {
            'fio': 'Шумилов Александр Владимирович',
            'foto': SimpleUploadedFile(name='test_image.jpg',
                                       content=
                                       open(
                                           'uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg',
                                           'rb').read(),
                                       content_type='image/jpeg'),
            'position': True,
            'salary': 200000,
            'age': 25,
        }
        employee = Employee.objects.create(
            **employee_data
        )
        response = self.client.post(path=URL_PATH + 'api/v1/department/',
                                    data={
                                        'name': 'УНЭ',
                                        'general': employee.id
                                        }
                                    )
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def tearDown(self):
        super().tearDown()


