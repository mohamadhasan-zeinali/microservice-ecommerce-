# Generated by Django 5.0.6 on 2024-06-15 08:44

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
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('description', models.CharField(max_length=300, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=3, max_digits=15, verbose_name='price')),
                ('stock', models.IntegerField(verbose_name='stock')),
            ],
        ),
    ]
