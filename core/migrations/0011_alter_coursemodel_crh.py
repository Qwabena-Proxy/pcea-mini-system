# Generated by Django 5.1.2 on 2025-04-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_coursemodel_crh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='crh',
            field=models.CharField(max_length=15),
        ),
    ]
