# Generated by Django 5.0.1 on 2024-01-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bistrokitchen_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='menuimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.IntegerField(choices=[(1, 'Starter'), (2, 'Breakfast'), (3, 'Lunch'), (4, 'Dinner')]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='details',
            field=models.CharField(max_length=100, verbose_name='Item Details'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Item Name'),
        ),
    ]
