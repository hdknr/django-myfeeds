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
    feeds = None 
    if id:
        feeds = models.Feed.objects.filter(id=id)
    elif url:
        feeds = [models.Feed.objects.get_or_create(url=url)]
    else:
        feeds = models.Feed.objects.all()

    for feed in feeds:
        feed.poll()


@main.command()
@click.pass_context
def list(ctx):
    for feed in models.Feed.objects.all():
        click.echo(f"{feed.id}. {feed.url} {feed.title}")
