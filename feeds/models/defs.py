from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from . import methods


class Timestamp(models.Model):
    created_at = models.DateTimeField(_('Created At'), default=now) 
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True


class Feed(Timestamp, methods.Feed):
    title = models.CharField(
        _('Feed Title'), max_length=1000, blank=True, null=True)
    url = models.URLField(
        _('Feed URL'), unique=True)
    link = models.URLField(
        _('Feed Link'), blank=True, null=True)
    description = models.TextField(
        _('Feed Description'), blank=True, null=True)

    published_at = models.DateTimeField(
        _('Feed Published At'), blank=True, null=True)
    last_polled_at = models.DateTimeField(
        _('Feed Last Polled At'), blank=True, null=True)

    class Meta:
        abstract = True


class Entry(Timestamp, methods.Entry):
    title = models.CharField(
        _('Entry Title'), max_length=2000, blank=True, null=True)
    link = models.URLField(
        _('Entry Link'), max_length=2000)
    description = models.TextField(
        _('Entry Description'), blank=True, null=True)
    published_at = models.DateTimeField(
        _('Entry Published At'), auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        abstract = True
