# Generated by Django 4.2.7 on 2023-12-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlibraryaccount',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
