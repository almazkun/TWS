# Generated by Django 3.0.7 on 2020-06-10 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0006_auto_20200610_1105")]

    operations = [
        migrations.AlterField(
            model_name="loanborrower",
            name="IIN",
            field=models.CharField(
                db_index=True,
                max_length=12,
                unique=True,
                verbose_name="Individual Identification Number",
            ),
        )
    ]
