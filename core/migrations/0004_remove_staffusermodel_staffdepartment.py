# Generated by Django 5.1.2 on 2025-04-04 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_staffusermodel_staffdepartment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffusermodel',
            name='staffDepartment',
        ),
    ]
