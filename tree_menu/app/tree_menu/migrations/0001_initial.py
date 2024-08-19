# Generated by Django 4.2.13 on 2024-05-10 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=150, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=150, null=True, verbose_name='Описание')),
                ('url', models.URLField(blank=True, max_length=60, verbose_name='URL ресурса пункта меню')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_item', to='tree_menu.category')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tree_menu.subcategory')),
            ],
            options={
                'verbose_name': 'Пункт меню',
                'verbose_name_plural': 'Пункты меню',
                'ordering': ('id',),
            },
        ),
    ]
