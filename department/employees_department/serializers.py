from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import (Department,
                     Employee)


class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    general = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(
            position=Employee.Position.GENERAL_MANAGER),
        allow_null=True,
        required=False)
    employee_count = serializers.IntegerField(read_only=True)
    salary_sum = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        departament = Department.objects.create(**validated_data)
        return departament

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',
                                           instance.name)
        instance.general = validated_data.get('general',
                                              instance.general)
        instance.save()
        return instance

    def to_representation(self, instance):
        general = super(DepartmentSerializer, self).to_representation(instance)
        if general and instance.general and instance.general.fio:
            general['general'] = instance.general.fio
        else:
            general['general'] = None
        return general


class EmployeeSerializer(serializers.Serializer):
    fio = serializers.CharField(max_length=200)
    foto = serializers.ImageField()
    position = serializers.ChoiceField(choices=Employee.Position.choices)
    salary = serializers.IntegerField(min_value=0)
    age = serializers.IntegerField(min_value=18,
                                   max_value=64)
    department = serializers.PrimaryKeyRelatedField(queryset=
                                                    Department.objects.all())

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fio = validated_data.get('fio',
                                          instance.fio)
        instance.foto = validated_data.get('foto',
                                           instance.foto)
        instance.position = validated_data.get('position',
                                               instance.position)
        instance.salary = validated_data.get('salary',
                                             instance.salary)
        instance.age = validated_data.get('age',
                                          instance.age)
        instance.department = validated_data.get('department',
                                                 instance.department)
        instance.save()
        return instance

    def to_representation(self, instance):
        employee = super(EmployeeSerializer, self).to_representation(instance)
        employee['department'] = instance.department.name
        employee['position'] = instance.get_position_display()
        return employee


