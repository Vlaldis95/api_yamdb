# Generated by Django 3.2 on 2023-07-03 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_title', '0003_alter_title_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название произвидения'),
        ),
    ]