# Generated by Django 4.2.5 on 2023-09-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_alter_task_expire_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='expire_at',
            field=models.DateTimeField(),
        ),
    ]