from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template import engines
from .. import models
from ..models import defs


def render(src, request=None, engine_name='django', safe=True, **ctx):
    text = engines[engine_name].from_string(src).render(ctx, request=request)
    return safe and mark_safe(text) or text


@admin.register(models.Feed)
class Feed(admin.ModelAdmin):
    list_display = [f.name for f in models.Feed._meta.fields]
    exclude = ['created_at']
    readonly_fields = ['updated_at']


@admin.register(models.Entry)
class Feed(admin.ModelAdmin):
    list_display = [
        f.name for f in models.Entry._meta.fields 
        if f.name not in ['description', 'link', 'created_at', 'updated_at']
    ]
    exclude = ['created_at', 'description', 'title', 'link']
    readonly_fields = ['updated_at', 'feed', 'title_and_link', 'html', 'navigates']
    list_filter = ['is_read']

    def navigates(self, obj):
        src = '''
        {% if prev_unread %}<p><a href="{% url 'admin:feeds_entry_change' prev_unread.id %}"> {{ prev_unread.id }}.{{ prev_unread }} </a> </p>{%  endif %}
        {% if next_unread %}<p><a href="{% url 'admin:feeds_entry_change' next_unread.id %}"> {{ next_unread.id }}.{{ next_unread }} </a> </p>{%  endif %}

        <hr>
        '''
        return render(src, next_unread=obj.next_unread, prev_unread=obj.prev_unread) 

    def title_and_link(self, obj):
        src = '''
            <a href="{{ link }}" target="_feed">{{ title}}</a>
        '''
        return render(src, title=obj.title, link=obj.link)

    def html(self, obj):
        return mark_safe(obj.description)