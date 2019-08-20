from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mytaggit.models import TaggableManager
from . import defs


class Feed(defs.Feed):

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.title or str(self.id)


class Entry(defs.Entry):
    feed = models.ForeignKey(Feed, verbose_name=_('Feed'), on_delete=models.CASCADE)

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-published_at', 'feed']
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    def __str__(self):
        return self.title or str(self.id)