# Generated by Django 5.0 on 2023-12-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees_department', '0004_alter_department_general_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='fio',
            field=models.CharField(db_index=True, max_length=200, verbose_name='ФИО'),
        ),
    ]
