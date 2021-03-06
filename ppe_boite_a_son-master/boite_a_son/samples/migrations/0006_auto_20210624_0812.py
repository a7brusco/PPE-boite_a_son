# Generated by Django 3.1.7 on 2021-06-24 08:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0005_auto_20210624_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 8, 12, 48, 888345, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 8, 12, 48, 886908, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sample',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 8, 12, 48, 887294, tzinfo=utc)),
        ),
    ]
