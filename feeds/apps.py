from django.apps import AppConfig as DjAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(DjAppConfig):
    name = 'feeds'
    verbose_name = _('Feeds')
