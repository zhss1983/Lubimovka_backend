# Generated by Django 3.2.12 on 2022-02-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0007_renaming_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=models.ImageField(help_text='Загрузите логотип партнёра', upload_to='images/info/partnerslogo', verbose_name='Логотип'),
        ),
    ]
