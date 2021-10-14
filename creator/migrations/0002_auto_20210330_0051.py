# Generated by Django 3.1.7 on 2021-03-30 00:51

import creator.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GetSurprizeContent',
            new_name='SurprizeLinkContent',
        ),
        migrations.AlterField(
            model_name='musiccontent',
            name='music',
            field=models.FileField(upload_to='music/', validators=[creator.models.validate_music_field]),
        ),
    ]