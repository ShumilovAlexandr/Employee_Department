from django.urls import (include,
                         path)
# from rest_framework import routers

from . import views


# router = routers.DefaultRouter()

# router.register(r'employee',
#                 views.EmployeeViewSet,
#                 basename='Employee')
# router.register(r'department',
#                 views.DepartmentViewSet,
#                 basename='Department')
#
# urlpatterns = router.urls
urlpatterns = [
    path('employee/<int:pk>/', views.EmployeeViewSet.as_view(),
         name='delete_employee'),
]