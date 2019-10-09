from django.db import models
from feeds import utils

class EntryQuerySet(models.QuerySet):

    def poll_for(self, feed):

        parsed = feed.poll()

        for i, entry in enumerate(parsed.entries):

            if not utils.is_valid_entry(entry):
                continue

            instance = self.filter(link=entry.link).first()

            if not instance:
                instance = self.create(
                    link=entry.link, 
                    published_at=utils.get_entry_published_time(entry),
                    title=utils.get_entry_title(entry),
                    description=utils.get_entry_description(entry), )

            instance.feeds.add(feed)
