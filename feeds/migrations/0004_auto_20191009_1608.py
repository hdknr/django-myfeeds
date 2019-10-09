# Generated by Django 2.2.4 on 2019-10-09 07:08

from django.db import migrations, models
import mytaggit.models


class Migration(migrations.Migration):

    dependencies = [
        ('mytaggit', '0006_auto_20190910_1407'),
        ('feeds', '0003_entry_trashed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['-published_at'], 'verbose_name': 'Entry', 'verbose_name_plural': 'Entries'},
        ),
        migrations.RemoveField(
            model_name='entry',
            name='feed',
        ),
        migrations.AddField(
            model_name='entry',
            name='feeds',
            field=models.ManyToManyField(blank=True, related_name='owner', to='feeds.Feed', verbose_name='Feed'),
        ),
        migrations.AddField(
            model_name='feed',
            name='tags',
            field=mytaggit.models.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='mytaggit.TaggedItem', to='mytaggit.Tag', verbose_name='Tags'),
        ),
    ]
