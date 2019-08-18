from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import feedparser
from feeds import utils


class Feed(object):

    def poll(self):
        parsed = feedparser.parse(self.url)
    
        if not utils.is_valid_feed(parsed):
            return
    
        self.published_at = utils.get_feed_published_time(parsed, self.published_at)
        self.title = utils.get_feed_title(parsed)
        self.description = utils.get_feed_description(parsed)
        self.link = parsed.feed.link
        self.last_polled_at = timezone.now()
        self.save()

        for i, entry in enumerate(parsed.entries):
            if not utils.is_valid_entry(entry):
                continue

            params = dict(
                published_at=utils.get_entry_published_time(entry),
                title=utils.get_entry_title(entry),
                description=utils.get_entry_description(entry), )

            if self.entry_set.filter(link=entry.link).update(**params) < 1:
                self.entry_set.create(link=entry.link, **params)

        return parsed

    @cached_property
    def last_feed(self):
        return self.poll()


class Entry(object):
    @cached_property
    def next_unread(self):
        return self.feed.entry_set.filter(id__gt=self.id, is_read=False).order_by('id').first()
    

    @cached_property
    def prev_unread(self):
        return self.feed.entry_set.filter(id__lt=self.id, is_read=False).order_by('id').last()