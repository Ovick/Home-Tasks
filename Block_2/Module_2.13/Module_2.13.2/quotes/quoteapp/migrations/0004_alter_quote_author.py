# Generated by Django 4.1.7 on 2023-03-04 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0003_alter_quote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoteapp.author'),
        ),
    ]