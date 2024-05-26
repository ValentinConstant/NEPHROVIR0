# Generated by Django 4.2.11 on 2024-05-13 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPP', '0009_test_bkv_peptide_activation_test_background_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='parameter_bio',
        ),
        migrations.AddField(
            model_name='test',
            name='integer_field',
            field=models.IntegerField(default='1'),
        ),
        migrations.AddField(
            model_name='test',
            name='power_field',
            field=models.IntegerField(choices=[(0, '0²'), (1, '1²'), (2, '2²'), (3, '3²'), (4, '4²'), (5, '5²'), (6, '6²'), (7, '7²'), (8, '8²')], default='2'),
        ),
    ]
