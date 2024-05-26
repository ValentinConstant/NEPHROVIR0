# Generated by Django 4.2.11 on 2024-05-13 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPP', '0010_remove_test_parameter_bio_test_integer_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='parameter_gen',
        ),
        migrations.RemoveField(
            model_name='test',
            name='parameter_immuno',
        ),
        migrations.RemoveField(
            model_name='test',
            name='power_field',
        ),
        migrations.AddField(
            model_name='test',
            name='BK_viral_load',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], default='4'),
        ),
        migrations.AddField(
            model_name='test',
            name='gen_sample_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='test',
            name='immuno_sample_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='test',
            name='mismatch_number',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')], default='4'),
        ),
    ]
