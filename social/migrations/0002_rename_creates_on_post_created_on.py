# Generated by Django 3.2.6 on 2021-08-04 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='creates_on',
            new_name='created_on',
        ),
    ]
