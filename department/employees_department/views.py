from rest_framework import viewsets
from rest_framework.response import Response

from .models import (Department,
                     Employee)
from .serializers import (EmployeeSerializer,
                          DepartmentSerializer)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


