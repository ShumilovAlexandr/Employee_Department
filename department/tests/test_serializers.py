from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import (Count,
                              Sum)

from employees_department.models import (Employee,
                                         Department)
from employees_department.serializers import (DepartmentSerializer,
                                              EmployeeSerializer)


class EmployeeDepartmentSerializerTest(TestCase):

    def setUp(self):
        self.department_data = {
            'name': 'УНДО'
        }
        self.department = Department.objects.create(
            **self.department_data
        )

        self.employee_data = {
            'fio': 'Иванов Иван Иванович',
            'foto': SimpleUploadedFile(name='test_image.jpg',
                                       content=
                                       open('uploads/1595243772_photo-of-man-taking-selfie-2406949.jpg',
                                           'rb').read(),
                                       content_type='image/jpeg'),
            'position': True,
            'salary': 200000,
            'age': 25,
            'department': self.department,
        }
        self.employee = Employee.objects.create(
            **self.employee_data
        )

        self.department.general = self.employee

        result = Employee.objects.all().aggregate(
            total_count=Count('fio'),
            total_salary=Sum('salary'))
        total_count = result['total_count']
        total_salary = result['total_salary']

        self.department.employee_count = total_count
        self.department.salary_sum = total_salary

        self.employee_serializer = EmployeeSerializer(instance=self.employee)
        self.department_serializer = DepartmentSerializer(instance=
                                                          self.department)

        self.data1 = self.employee_serializer.data
        self.data2 = self.department_serializer.data

    def test_contains_expected_fields(self):

        self.assertEqual(set(self.data1.keys()),
                         set(['fio',
                              'foto',
                              'position',
                              'salary',
                              'age',
                              'department']))
        self.assertEqual(set(self.data2),
                         set(['name',
                              'general',
                              'employee_count',
                              'salary_sum']))

    def test_field_content(self):
        self.assertEqual(self.data1['fio'], self.employee_data['fio'])
        self.assertEqual(self.data1['foto'][9:19],
                         str(self.employee_data['foto'])[:-4])
        self.assertEqual(self.data1['position'], 'Директор')
        self.assertEqual(self.data1['salary'], self.employee_data['salary'])
        self.assertEqual(self.data1['age'], self.employee_data['age'])
        self.assertEqual(self.data1['department'],
                         str(self.employee_data['department']))
        self.assertEqual(self.data2['name'], self.department_data['name'])
        self.assertEqual(self.data2['general'],
                         str(self.department.general))

        self.assertEqual(self.data2['employee_count'],
                         self.department.employee_count)
        self.assertEqual(self.data2['salary_sum'],
                         self.department.salary_sum)

    def test_position_must_be_in_choice(self):
        self.assertEqual(self.employee.position,
                         Employee.Position.GENERAL_MANAGER)

    def tearDown(self):
        super().tearDown()

