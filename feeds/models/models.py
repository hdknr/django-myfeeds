from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mytaggit.models import TaggableManager
from . import defs, querysets


class Feed(defs.Feed):

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.title or str(self.id)


class Entry(defs.Entry):

    feeds = models.ManyToManyField(
        Feed, related_name='owner', verbose_name=_('Feed'), blank=True,)

    tags = TaggableManager(blank=True)

    objects = querysets.EntryQuerySet.as_manager()

    class Meta:
        ordering = ['-published_at', ]
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    def __str__(self):
        return self.title or str(self.id)
