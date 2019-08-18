import djclick as click
from django.db.models import Q
from django.utils import translation, timezone
from datetime import datetime, timedelta, time
from feeds import models
from logging import getLogger
log = getLogger()

translation.activate('ja')


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--id', '-i', default=None)
@click.option('--url', '-u', default=None)
@click.pass_context
def poll(ctx, id, url):
    feed = None 
    if id:
        feed = models.Feed.objects.filter(id=id).first()
    elif url:
        feed, created = models.Feed.objects.get_or_create(url=url)

    feed and feed.poll()


@main.command()
@click.pass_context
def list(ctx):
    for feed in models.Feed.objects.all():
        click.echo(f"{feed.id}. {feed.url} {feed.title}")
