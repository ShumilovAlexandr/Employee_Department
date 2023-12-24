from django.db import models
from django.core.validators import MinLengthValidator


class Employee(models.Model):

    class Position(models.IntegerChoices):
        ORDINARY_EMPLOYEE = (0, 'Сотрудник')
        GENERAL_MANAGER = (1, 'Директор')

    fio = models.CharField(max_length=200,
                           db_index=True,
                           verbose_name='ФИО')
    foto = models.ImageField(upload_to='uploads/',
                             verbose_name='Фото')
    position = models.BooleanField(choices=Position.choices,
                                   default=Position.ORDINARY_EMPLOYEE,
                                   verbose_name='Должность')
    salary = models.IntegerField(
        validators=[MinLengthValidator(limit_value=0)],
        verbose_name='Зарплата'
    )
    age = models.IntegerField(
        validators=[MinLengthValidator(limit_value=18)],
        verbose_name='Возраст'
    )
    department = models.ForeignKey('Department',
                                   on_delete=models.CASCADE,
                                   related_name='employee',
                                   blank=True,
                                   null=True,
                                   verbose_name='Департамент')

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        unique_together = ["fio", "department"]


class Department(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название департамента')
    general = models.OneToOneField(Employee,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   limit_choices_to=
                                   {"position":
                                    Employee.Position.GENERAL_MANAGER},
                                   verbose_name='Руководитель',
                                   related_name='general')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

