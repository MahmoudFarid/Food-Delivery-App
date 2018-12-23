# Generated by Django 2.1.2 on 2018-12-23 15:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import food_delivery_app.restaurants.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Item category',
                'verbose_name_plural': 'Item categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128)),
                ('short_description', models.CharField(max_length=128)),
                ('image', models.ImageField(blank=True, null=True, upload_to=food_delivery_app.restaurants.models.item_images)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='restaurants.Category')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemOrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Item size',
                'verbose_name_plural': 'Item sizes',
            },
        ),
        migrations.CreateModel(
            name='ItemSizeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_details', to='restaurants.Item')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_details', to='restaurants.ItemSize')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('address', models.CharField(max_length=500)),
                ('status', models.IntegerField(choices=[(1, 'Picked'), (2, 'Cooking'), (3, 'Ready'), (4, 'On the way'), (5, 'Delivered'), (6, 'Candelled')], default=1)),
                ('total_price', models.IntegerField(default=0)),
                ('cooked_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('items_sizes', models.ManyToManyField(related_name='orders', through='restaurants.ItemOrderDetails', to='restaurants.ItemSizeDetails')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('phone', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone')),
                ('address', models.CharField(max_length=128, verbose_name='Address')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=food_delivery_app.restaurants.models.restaurant_images, verbose_name='Logo')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_restaurants', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='restaurants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='itemsize',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_sizes', to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='itemorderdetails',
            name='item_size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders_details', to='restaurants.ItemSizeDetails'),
        ),
        migrations.AddField(
            model_name='itemorderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_details', to='restaurants.Order'),
        ),
        migrations.AddField(
            model_name='item',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='item',
            name='sizes',
            field=models.ManyToManyField(related_name='items', through='restaurants.ItemSizeDetails', to='restaurants.ItemSize'),
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='restaurants.Restaurant'),
        ),
        migrations.AlterUniqueTogether(
            name='itemsizedetails',
            unique_together={('item', 'size')},
        ),
        migrations.AlterUniqueTogether(
            name='itemsize',
            unique_together={('name', 'restaurant')},
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'restaurant')},
        ),
    ]
