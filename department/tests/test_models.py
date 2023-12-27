from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from employees_department.models import (Employee,
                                         Department)


class EmployeeDepartmentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = Department.objects.create(
            name='УНДО',
        )
        cls.employee = Employee.objects.create(
            fio='Шумилов Александр Владимирович',
            foto=SimpleUploadedFile(name='test_image.jpg',
                                    content=open(
                                        'uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg', 'rb').read(),
                                    content_type='image/jpeg'),
            position=True,
            salary=200000,
            age=25,
            department=cls.department,
            )
        cls.department.general = cls.employee
        cls.department.save()
        cls.employee.save()

    def test_verbose_name(self):
        employee = EmployeeDepartmentModelTest.employee
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
                    employee._meta.get_field(field).verbose_name, expected
                )

    def test_may_be_several_employees_in_the_department(self):
        employee = EmployeeDepartmentModelTest.employee
        department = EmployeeDepartmentModelTest.department
        self.assertIsInstance(employee.department, Department)
        self.assertIsInstance(department.general, Employee)


