# Generated by Django 3.0.4 on 2020-06-09 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200609_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanborrower',
            name='dob',
            field=models.DateField(default='0001-01-01', verbose_name='Date of Birth'),
        ),
    ]