import graphene

from graphene_django import DjangoObjectType

from .models import (Employee,
                     Department)


class EmployeeType(DjangoObjectType):
    position = graphene.String()

    class Meta:
        model = Employee
        fields = '__all__'

    def resolve_position(self, info, **kwargs):
        return self.get_position_display()


class DepartmentType(DjangoObjectType):
    employee_count = graphene.Int()
    salary_sum = graphene.Int()

    class Meta:
        model = Department
        fields = '__all__'

    def resolve_employee_count(self, info):
        count = self.employee.count()
        return count

    def resolve_salary_sum(self, info):
        result = sum([employee.salary for employee in
                      self.employee.all()])
        return result

