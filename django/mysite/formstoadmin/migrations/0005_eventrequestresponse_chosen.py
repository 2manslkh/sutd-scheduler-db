# Generated by Django 2.2 on 2019-04-24 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formstoadmin', '0004_remove_eventrequestresponse_chosen'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventrequestresponse',
            name='chosen',
            field=models.BooleanField(null=True),
        ),
    ]
