import graphene

from graphene_django.rest_framework.mutation import SerializerMutation

from .types import (EmployeeType,
                    DepartmentType)
from .models import (Employee,
                     Department)
from .serializers import EmployeeSerializer


class CreateDepartmentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, name):
        department = Department(name=name)
        department.save()
        return CreateDepartmentMutation(department=department)


class UpdateDepartmentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        general = graphene.ID(required=True)

    department = graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        department = Department.objects.get(pk=kwargs["id"])
        employee_instance = Employee.objects.get(pk=kwargs["general"])
        if employee_instance.position == 1:
            department.name = kwargs["name"]
            department.general = employee_instance

            department.save()
            return UpdateDepartmentMutation(department=department)
        else:
            raise Exception("Назначен руководителем может быть только "
                            "сотрудник с соответствующей должностью!")


class CreateEmployeeMutation(graphene.Mutation):
    class Arguments:
        fio = graphene.String()
        foto = graphene.String()
        position = graphene.Int()
        salary = graphene.Int()
        age = graphene.Int()
        department = graphene.ID(required=True)

    employee = graphene.Field(EmployeeType)

    @classmethod
    def mutate(cls, root, info, fio, foto, position, salary, age, department):
        department_instance = Department.objects.get(pk=department)

        employee = Employee(fio=fio,
                            foto=foto,
                            position=position,
                            salary=salary,
                            age=age,
                            department=department_instance)
        employee.save()
        return CreateEmployeeMutation(employee=employee)


class DeleteEmployeeMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    employee = graphene.Field(EmployeeType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        employee = Employee.objects.get(pk=kwargs["id"])
        employee.delete()
        return cls(ok=True)
