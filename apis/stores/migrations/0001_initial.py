# Generated by Django 5.1.6 on 2025-04-03 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Store name', max_length=255, unique=True)),
                ('type', models.CharField(choices=[('restaurants', 'Restaurants'), ('grocery', 'Grocery'), ('garment', 'Garment'), ('electronics', 'Electronics'), ('furniture', 'Furniture'), ('books', 'Books'), ('other', 'Other')], default='other', help_text='Type of store (e.g., Grocery, Garment, Electronics, etc.)', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Short description of the store', null=True)),
                ('address', models.TextField(help_text='Full address of the store')),
                ('city', models.CharField(help_text='City where the store is located', max_length=100)),
                ('state', models.CharField(help_text='State where the store is located', max_length=100)),
                ('pincode', models.CharField(help_text='Postal code of the store', max_length=10)),
                ('phone', models.CharField(blank=True, help_text='Store contact number', max_length=20, null=True)),
                ('email', models.EmailField(blank=True, help_text='Store email address', max_length=254, null=True)),
                ('opening_time', models.TimeField(help_text='Opening time of the store')),
                ('closing_time', models.TimeField(help_text='Closing time of the store')),
                ('is_active', models.BooleanField(default=True, help_text='Whether the store is active or not')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Time when the store was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated timestamp')),
                ('owner', models.ForeignKey(help_text='User who owns the store.', limit_choices_to={'role': 'shop_owner'}, on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
                'ordering': ['-created_at'],
            },
        ),
    ]
