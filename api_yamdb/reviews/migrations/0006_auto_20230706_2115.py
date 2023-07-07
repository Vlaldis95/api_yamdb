# Generated by Django 3.2 on 2023-07-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230706_2113'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_title_author',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_title_author'),
        ),
    ]
