# Generated by Django 3.1.3 on 2022-03-02 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_free_trial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
