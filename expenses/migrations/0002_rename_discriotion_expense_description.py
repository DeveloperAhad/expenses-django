# Generated by Django 3.2.6 on 2021-10-30 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='discriotion',
            new_name='description',
        ),
    ]
