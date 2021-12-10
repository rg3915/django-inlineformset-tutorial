# Generated by Django 3.2.10 on 2021-12-08 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='título')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='preço')),
                ('manufacturing_date', models.DateField(blank=True, null=True, verbose_name='data de fabricação')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='data de vencimento')),
            ],
            options={
                'verbose_name': 'produto',
                'verbose_name_plural': 'produtos',
                'ordering': ('title',),
            },
        ),
    ]
