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
    actions = ['mark_as_read', 'mark_as_trashed']

    def navigates(self, obj):
        src = '''
        {% if prev_unread %}<p><a href="{% url 'admin:feeds_entry_change' prev_unread.id %}"> {{ prev_unread.id }}.{{ prev_unread }} </a> </p>{%  endif %}
        {% if next_unread %}<p><a href="{% url 'admin:feeds_entry_change' next_unread.id %}"> {{ next_unread.id }}.{{ next_unread }} </a> </p>{%  endif %}
        '''
        return render(src, current=obj, next_unread=obj.next_unread, prev_unread=obj.prev_unread) 

    def title_and_link(self, obj):
        src = '''
            <a href="{{ link }}" target="_feed"><i class="fas fa-external-link-alt"></i></a> &nbsp;
            <span>{{ current.title }}</span>&nbsp;
            <a href="#" class="markdown" title="{{ current.markdown_link}}"><i class="far fa-copy"></i></a>
        '''
        return render(src, current=obj, link=obj.link)

    def html(self, obj):
        return mark_safe(obj.description)

    def mark_as_read(self, request, queryset):
        counts = queryset.update(is_read=True)
        self.message_user(request, f"{counts} successfully marked as read.")

    mark_as_read.short_description = _('Mark as Read')

    def mark_as_trashed(self, request, queryset):
        counts = queryset.update(is_read=True, trashed=True)
        self.message_user(request, f"{counts} successfully marked as trashed.")

    mark_as_trashed.short_description = _('Mark as Trashed')