# Generated by Django 3.1.7 on 2021-06-28 16:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0008_auto_20210624_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='typeOfMusic',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collection',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 16, 13, 52, 459542, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 16, 13, 52, 458212, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='sample',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 16, 13, 52, 458562, tzinfo=utc)),
        ),
    ]