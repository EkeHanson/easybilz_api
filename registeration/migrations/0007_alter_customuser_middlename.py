# Generated by Django 5.0.2 on 2024-08-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registeration', '0006_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middleName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
