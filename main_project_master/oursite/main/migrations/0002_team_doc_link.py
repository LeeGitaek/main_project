# Generated by Django 2.1.7 on 2019-04-09 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='doc_link',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
