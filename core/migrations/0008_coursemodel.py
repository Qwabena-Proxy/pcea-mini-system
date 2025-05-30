# Generated by Django 5.1.2 on 2025-04-09 08:25

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_levelmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='courseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=uuid.uuid4, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=15, unique=True)),
                ('semester', models.CharField(max_length=5)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.levelmodel')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.programemodel')),
            ],
        ),
    ]
