# Generated by Django 5.1.7 on 2025-03-20 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_redirecionado', models.URLField()),
                ('url_personalizado', models.CharField(max_length=8, unique=True)),
            ],
        ),
    ]
