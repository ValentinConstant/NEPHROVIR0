# Generated by Django 4.2.11 on 2024-05-12 23:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPP', '0007_alter_lotdetest_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotdetest',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lotdetest',
            name='numero_lot',
            field=models.CharField(max_length=4, unique=True, validators=[django.core.validators.MaxLengthValidator(4), django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator('^[0-9]*$', message='Le numéro de lot doit être composé uniquement de chiffres.')]),
        ),
        migrations.AlterField(
            model_name='test',
            name='serial_number',
            field=models.CharField(max_length=4),
        ),
    ]