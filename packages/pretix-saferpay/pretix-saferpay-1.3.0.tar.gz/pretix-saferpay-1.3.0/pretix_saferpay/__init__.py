from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class PluginApp(AppConfig):
    name = 'pretix_saferpay'
    verbose_name = 'Saferpay (SIX) implementation for pretix'

    class PretixPluginMeta:
        name = gettext_lazy('Saferpay (SIX)')
        author = 'Raphael Michel'
        category = 'PAYMENT'
        description = gettext_lazy('This allows to accept payments through saferpay.')
        visible = True
        version = '1.3.0'

    def ready(self):
        from . import signals, tasks  # NOQA


default_app_config = 'pretix_saferpay.PluginApp'
