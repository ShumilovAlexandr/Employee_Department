import graphene

from django.db.models import Q

from .models import (Employee,
                     Department)
from .types import (EmployeeType,
                    DepartmentType)
from .mutations import (CreateDepartmentMutation,
                        CreateEmployeeMutation,
                        DeleteEmployeeMutation,
                        UpdateDepartmentMutation)


class Query(graphene.ObjectType):
    # для получения списка сотрудников с пагинацией и поиском по фамилии
    employees = graphene.List(
        EmployeeType,
        first=graphene.Int(),
        skip=graphene.Int(),
        search=graphene.String()
    )
    # Для получения отдельного сотрудника по id
    employee = graphene.Field(EmployeeType,
                              id=graphene.Int(required=True))
    # Для получения списка департаментов и поиска (фильтрации) департамента по
    # его id
    department = graphene.List(
        DepartmentType,
        search=graphene.Int()
    )

    def resolve_employees(self,
                          info,
                          first=None,
                          skip=None,
                          search=None,
                          **kwargs):
        employee = Employee.objects.all()
        user = info.context.user
        if user.is_authenticated:
            if search:
                filter = (
                    Q(fio__icontains=search)
                )
                return Employee.objects.filter(filter)
            if skip:
                employee = employee[skip:]
            if first:
                employee = employee[:first]
            return employee
        raise Exception('Ошибка аутентификации: Вы должны войти в систему')

    def resolve_employee(self, info, id, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            return Employee.objects.get(pk=id)
        raise Exception('Ошибка аутентификации: Вы должны войти в систему')

    def resolve_department(self,
                           info,
                           search=None,
                           **kwargs):
        if search:
            filter = (
                Q(pk=search)
            )
            return Department.objects.filter(filter)

        return Department.objects.all()


class Mutation(graphene.ObjectType):
    create_department = CreateDepartmentMutation.Field()
    update_department = UpdateDepartmentMutation.Field()
    create_employee = CreateEmployeeMutation.Field()
    delete_employee = DeleteEmployeeMutation.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutation)
