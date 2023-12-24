from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import (Count,
                              Sum)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from .models import (Department,
                     Employee)
from .serializers import (EmployeeSerializer,
                          DepartmentSerializer)
from .pagination import EmployeePagination


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fio', 'department__id']
    pagination_class = EmployeePagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [AllowAny()]


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('general').\
            annotate(employee_count=Count('general__fio'),
                     salary_sum=Sum('employee__salary')
                     )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


