# Generated by Django 4.1 on 2022-08-14 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_submituser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submituser',
            name='lastSubmitDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
