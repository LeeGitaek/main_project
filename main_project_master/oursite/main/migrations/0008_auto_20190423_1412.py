# Generated by Django 2.1.7 on 2019-04-23 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_reviewbox_review_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewbox',
            name='review_score',
            field=models.FloatField(default=0.0),
        ),
    ]
