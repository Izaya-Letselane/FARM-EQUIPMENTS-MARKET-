# Generated by Django 5.0.1 on 2024-03-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0005_alter_product_productname'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='productName',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
