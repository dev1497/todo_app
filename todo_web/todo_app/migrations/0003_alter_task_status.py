# Generated by Django 4.2.5 on 2023-09-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Done', 'D'), ('Not Done', 'ND')], max_length=10),
        ),
    ]