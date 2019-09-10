from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template import engines
from .. import models
from ..models import defs
from . import inlines


def render(src, request=None, engine_name='django', safe=True, **ctx):
    text = engines[engine_name].from_string(src).render(ctx, request=request)
    return safe and mark_safe(text) or text


@admin.register(models.Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Feed._meta.fields]
    exclude = ['created_at']
    readonly_fields = ['updated_at']


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in models.Entry._meta.fields 
        if f.name not in ['description', 'link', 'created_at', 'updated_at']
    ]
    exclude = ['created_at', 'description', 'title', 'link']
    readonly_fields = [
        'updated_at', 'feed', 
        'title_and_link', 'html', 'navigates']
    list_filter = ['is_read']
    inlines = [
        inlines.EntryTagItemInline,
    ]
    search_fields = ['title', 'description']

    def navigates(self, obj):
        src = '''
        {% if prev_unread %}<p><a href="{% url 'admin:feeds_entry_change' prev_unread.id %}"> {{ prev_unread.id }}.{{ prev_unread }} </a> </p>{%  endif %}
        {% if next_unread %}<p><a href="{% url 'admin:feeds_entry_change' next_unread.id %}"> {{ next_unread.id }}.{{ next_unread }} </a> </p>{%  endif %}
        '''
        return render(src, current=obj, next_unread=obj.next_unread, prev_unread=obj.prev_unread) 

    def title_and_link(self, obj):
        title = '<i class="fas fa-external-link-alt"></i>'
        src = '''
            <a href="{{ link }}" target="_feed">{{ title|safe }}</a> &nbsp;
            <span class="markdown">{{ current.markdown_link}}</span>
        '''
        return render(src, current=obj, title=title, link=obj.link)

    def html(self, obj):
        return mark_safe(obj.description)