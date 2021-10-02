# Generated by Django 3.2.7 on 2021-10-02 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_person_image'),
        ('info', '0003_remove_festival_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.person', verbose_name='Человек'),
        ),
    ]
