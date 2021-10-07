# Generated by Django 3.1.7 on 2021-06-28 17:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0010_auto_20210628_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 17, 12, 58, 575738, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 17, 12, 58, 574443, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='typeOfMusic',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='sample',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 17, 12, 58, 574790, tzinfo=utc)),
        ),
    ]