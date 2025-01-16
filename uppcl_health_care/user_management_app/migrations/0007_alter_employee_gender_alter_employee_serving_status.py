# Generated by Django 5.1.3 on 2024-12-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_app', '0006_alter_employee_gender_alter_employee_serving_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='M', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='serving_status',
            field=models.CharField(blank=True, choices=[('Serving', 'Serving'), ('Retired', 'Retired')], default='Serving', max_length=8, null=True),
        ),
    ]
