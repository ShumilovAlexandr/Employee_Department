from abc import ABC

from rest_framework import serializers

from .models import (Department,
                     Employee)


# Тут тупо можно использовать ModelSerializer, но я пошел по другому пути
class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    general = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all())

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',
                                           instance.name)
        instance.general = validated_data.get('general',
                                              instance.general)
        instance.save()
        return instance


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

