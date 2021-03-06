# Generated by Django 2.2.7 on 2019-11-27 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='title',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='news',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.Thread'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='phonograms',
            field=models.TextField(blank=True),
        ),
    ]
