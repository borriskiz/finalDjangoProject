# Generated by Django 4.2.16 on 2024-11-06 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coindb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coins', to='coindb.shop', verbose_name='Shop'),
        ),
    ]
