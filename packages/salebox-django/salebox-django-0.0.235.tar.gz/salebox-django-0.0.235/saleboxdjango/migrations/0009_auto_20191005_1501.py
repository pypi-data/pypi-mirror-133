# Generated by Django 2.1.8 on 2019-10-05 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saleboxdjango', '0008_auto_20191005_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countrystatetranslation',
            name='state',
        ),
        migrations.RemoveField(
            model_name='countrytranslation',
            name='country',
        ),
        migrations.DeleteModel(
            name='CountryStateTranslation',
        ),
        migrations.DeleteModel(
            name='CountryTranslation',
        ),
    ]
