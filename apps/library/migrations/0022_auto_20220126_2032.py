# Generated by Django 3.2.11 on 2022-01-26 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_auto_20220118_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherplay',
            name='name',
            field=models.CharField(max_length=70, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='play',
            name='name',
            field=models.CharField(max_length=70, unique=True, verbose_name='Название пьесы'),
        ),
    ]
