# Generated by Django 2.2.1 on 2019-05-09 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='holiday_type',
            field=models.CharField(choices=[('public', 'Public Holiday'), ('national', 'National Holiday')], max_length=12),
        ),
    ]
