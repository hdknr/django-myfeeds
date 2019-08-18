# Generated by Django 2.2.3 on 2019-08-14 07:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import feeds.models.methods


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Feed Title')),
                ('url', models.URLField(unique=True, verbose_name='Feed URL')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Feed Link')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Feed Description')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Feed Published At')),
                ('last_polled_at', models.DateTimeField(blank=True, null=True, verbose_name='Feed Last Polled At')),
            ],
            options={
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
            bases=(models.Model, feeds.models.methods.Feed),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('title', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Entry Title')),
                ('link', models.URLField(max_length=2000, verbose_name='Entry Link')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Entry Description')),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Entry Published At')),
                ('is_read', models.BooleanField(default=False)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feeds.Feed', verbose_name='Feed')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
                'ordering': ['-published_at', 'feed'],
            },
            bases=(models.Model, feeds.models.methods.Entry),
        ),
    ]