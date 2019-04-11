# Generated by Django 2.1.7 on 2019-04-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('class_type', models.CharField(max_length=200)),
                ('class_related', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=200)),
                ('others', models.CharField(max_length=200)),
                ('makeup', models.CharField(max_length=200)),
                ('assigned_Professors', models.CharField(max_length=200)),
                ('course_Lead', models.CharField(max_length=200)),
                ('Cohort_Size', models.CharField(max_length=200)),
                ('Enrolment_Size', models.CharField(max_length=200)),
            ],
        ),
    ]
