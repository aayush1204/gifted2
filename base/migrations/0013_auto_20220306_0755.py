# Generated by Django 3.1.3 on 2022-03-06 07:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20220306_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='due_time',
            field=models.TimeField(default=datetime.time(10, 10)),
        ),
    ]