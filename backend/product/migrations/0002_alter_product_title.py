# Generated by Django 3.2.10 on 2021-12-09 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=20, unique=True, verbose_name='título'),
        ),
    ]
