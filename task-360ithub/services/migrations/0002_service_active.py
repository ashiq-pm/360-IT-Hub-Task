# Generated by Django 5.1.1 on 2024-09-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
