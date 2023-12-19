from rest_framework import generics
from rest_framework.response import Response

from .models import (Department,
                     Employee)
from .serializers import (EmployeeSerializer,
                          DepartmentSerializer)

# Так работает метод добавления и удаления. Нужно сделать нормальную
# документацию
class EmployeeViewSet(generics.DestroyAPIView,
                      generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


# class DepartmentViewSet(viewsets.ModelViewSet):
#     serializer_class = DepartmentSerializer
#     queryset = Department.objects.all()


