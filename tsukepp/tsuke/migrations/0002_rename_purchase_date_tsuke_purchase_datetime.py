# Generated by Django 4.2.5 on 2023-09-20 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsuke', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tsuke',
            old_name='purchase_date',
            new_name='purchase_datetime',
        ),
    ]