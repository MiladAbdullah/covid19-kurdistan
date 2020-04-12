# Generated by Django 3.0.5 on 2020-04-11 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=30, verbose_name="patient's full name")),
                ('blood_group', models.PositiveSmallIntegerField(choices=[(0, 'A+'), (1, 'B+'), (2, 'AB+'), (3, 'O+'), (4, 'A-'), (5, 'B-'), (6, 'AB-'), (7, 'O-')])),
            ],
        ),
    ]