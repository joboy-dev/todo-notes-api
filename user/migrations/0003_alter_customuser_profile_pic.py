# Generated by Django 4.1.7 on 2023-03-30 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default.PNG', null=True, upload_to='profile_pics'),
        ),
    ]
