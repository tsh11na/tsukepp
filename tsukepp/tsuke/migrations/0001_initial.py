# Generated by Django 4.2.5 on 2023-09-20 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tsuke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True, verbose_name='購入日時')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='金額')),
                ('is_paid', models.BooleanField(default=False, verbose_name='支払')),
                ('note', models.CharField(blank=True, max_length=50, verbose_name='メモ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
    ]
