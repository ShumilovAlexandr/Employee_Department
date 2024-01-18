from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from employees_department.models import (Employee,
                                         Department)


class EmployeeDepartmentModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name='УНДО',
        )
        self.employee = Employee.objects.create(
            fio='Иванов Иван Иванович',
            foto=SimpleUploadedFile(name='test_image.jpg',
                                    content=open(
                                        'uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg', 'rb').read(),
                                    content_type='image/jpeg'),
            position=True,
            salary=200000,
            age=25,
            department=self.department,
            )
        self.department.general = self.employee
        self.department.save()
        self.employee.save()

    def test_verbose_name(self):
        empl = self.employee
        field_verbose = {
            'fio': 'ФИО',
            'foto': 'Фото',
            'position': 'Должность',
            'salary': 'Зарплата',
            'age': 'Возраст',
            'department': 'Департамент',
        }
        for field, expected in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    empl._meta.get_field(field).verbose_name, expected
                )

    def test_may_be_several_employees_in_the_department(self):
        employee = self.employee
        department = self.department
        self.assertIsInstance(employee.department, Department)
        self.assertIsInstance(department.general, Employee)

    def tearDown(self):
        super().tearDown()


