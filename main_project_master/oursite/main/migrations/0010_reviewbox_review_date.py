# Generated by Django 2.1.7 on 2019-04-23 06:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190423_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewbox',
            name='review_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]