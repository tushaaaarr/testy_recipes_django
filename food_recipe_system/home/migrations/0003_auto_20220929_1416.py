# Generated by Django 3.1.7 on 2022-09-29 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220927_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 29, 14, 16, 18, 270962)),
        ),
        migrations.AlterField(
            model_name='recipeimage',
            name='images',
            field=models.FileField(upload_to='media'),
        ),
    ]
