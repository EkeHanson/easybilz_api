# Generated by Django 5.0.2 on 2024-07-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registeration', '0005_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True),
        ),
    ]
