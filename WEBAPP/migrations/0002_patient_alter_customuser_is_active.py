# Generated by Django 4.2.11 on 2024-04-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=100, verbose_name='Identifiant du Patient')),
                ('sex', models.CharField(choices=[('M', 'Homme'), ('F', 'Femme')], max_length=1, verbose_name='Sexe')),
                ('birth_date', models.DateField(verbose_name='Date de naissance')),
                ('hospital', models.CharField(max_length=100, verbose_name='Hôpital')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]