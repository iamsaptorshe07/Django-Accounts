# Generated by Django 2.2 on 2020-06-17 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Open Blog Forum User', max_length=100),
        ),
    ]