# Generated by Django 5.0.2 on 2024-03-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prev_card',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
