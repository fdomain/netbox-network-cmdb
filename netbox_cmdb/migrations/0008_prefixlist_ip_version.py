# Generated by Django 3.2.8 on 2021-12-13 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_cmdb', '0007_routepolicyterm_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefixlist',
            name='ip_version',
            field=models.CharField(default='ipv4', max_length=10),
        ),
    ]
