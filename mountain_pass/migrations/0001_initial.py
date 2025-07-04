# Generated by Django 5.2.3 on 2025-06-23 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(blank=True, choices=[('1A', '1A'), ('2A', '2A'), ('3A', '3A'), ('4A', '4A')], max_length=2)),
                ('summer', models.CharField(blank=True, choices=[('1A', '1A'), ('2A', '2A'), ('3A', '3A'), ('4A', '4A')], max_length=2)),
                ('autumn', models.CharField(blank=True, choices=[('1A', '1A'), ('2A', '2A'), ('3A', '3A'), ('4A', '4A')], max_length=2)),
                ('spring', models.CharField(blank=True, choices=[('1A', '1A'), ('2A', '2A'), ('3A', '3A'), ('4A', '4A')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('fam', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('otc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MountainPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('other_titles', models.CharField(max_length=255)),
                ('connect', models.TextField(blank=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'Новый'), ('pending', 'В работе'), ('accepted', 'Принят'), ('rejected', 'Отклонен')], default='new', max_length=10)),
                ('coords', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mountain_pass.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mountain_pass.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mountain_pass.user')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='mountain_passes/')),
                ('mountain_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mountain_pass.mountainpass')),
            ],
        ),
    ]
