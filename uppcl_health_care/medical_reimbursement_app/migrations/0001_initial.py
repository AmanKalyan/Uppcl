# Generated by Django 5.1.3 on 2024-12-17 06:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management_app', '0007_alter_employee_gender_alter_employee_serving_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalReimbursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_type', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], max_length=10)),
                ('hospital_name', models.CharField(blank=True, max_length=255, null=True)),
                ('hospital_type', models.CharField(blank=True, max_length=50, null=True)),
                ('income_tax_exempt', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reimbursements', to='user_management_app.employee')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reimbursements', to='user_management_app.dependent')),
            ],
        ),
        migrations.CreateModel(
            name='IndoorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_entitled', models.CharField(blank=True, choices=[('General', 'General'), ('Semi Private', 'Semi Private'), ('Private', 'Private')], max_length=20, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('treating_doctor', models.CharField(blank=True, max_length=255, null=True)),
                ('admission_date', models.DateField(blank=True, null=True)),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('accommodation_general', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('accommodation_semi_private', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('accommodation_private', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('accommodation_icu', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('investigations', models.TextField(blank=True, null=True)),
                ('procedures', models.TextField(blank=True, null=True)),
                ('medicines_consumables', models.TextField(blank=True, null=True)),
                ('implants', models.TextField(blank=True, null=True)),
                ('other_charges', models.TextField(blank=True, null=True)),
                ('total_expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reimbursement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='indoor_details', to='medical_reimbursement_app.medicalreimbursement')),
            ],
        ),
        migrations.CreateModel(
            name='OutdoorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_entitled', models.CharField(blank=True, choices=[('General', 'General'), ('Semi Private', 'Semi Private'), ('Private', 'Private')], max_length=20, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('treating_doctor', models.CharField(blank=True, max_length=255, null=True)),
                ('long_term_illness', models.TextField(blank=True, null=True)),
                ('treatment_period_from', models.DateField(blank=True, null=True)),
                ('treatment_period_to', models.DateField(blank=True, null=True)),
                ('dialysis', models.BooleanField(default=False)),
                ('chemotherapy', models.BooleanField(default=False)),
                ('radiotherapy', models.BooleanField(default=False)),
                ('emergency_treatment', models.BooleanField(default=False)),
                ('diagnostic_tests', models.TextField(blank=True, null=True)),
                ('hearing_aids_denture', models.BooleanField(default=False)),
                ('anti_rabies_treatment', models.BooleanField(default=False)),
                ('other_charges', models.TextField(blank=True, null=True)),
                ('total_expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reimbursement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='outdoor_details', to='medical_reimbursement_app.medicalreimbursement')),
            ],
        ),
    ]
