# Generated by Django 4.2.9 on 2024-01-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_mail_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseemail',
            name='attachment',
            field=models.FileField(upload_to=''),
        ),
    ]
