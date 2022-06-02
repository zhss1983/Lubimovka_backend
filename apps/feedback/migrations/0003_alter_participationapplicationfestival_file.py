# Generated by Django 3.2.13 on 2022-06-02 14:12

import apps.feedback.utilities
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_alter_participationapplicationfestival_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participationapplicationfestival',
            name='file',
            field=models.FileField(blank=True, help_text="Файл в одном из форматов ('doc', 'docx', 'txt', 'odt', 'pdf')", upload_to=apps.feedback.utilities.generate_upload_path, validators=[django.core.validators.FileExtensionValidator(('doc', 'docx', 'txt', 'odt', 'pdf'))], verbose_name='Файл'),
        ),
    ]
