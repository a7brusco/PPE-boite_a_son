# Generated by Django 3.1.7 on 2021-06-12 09:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 12, 9, 13, 42, 846532, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sample',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 12, 9, 13, 42, 845479, tzinfo=utc)),
        ),
    ]