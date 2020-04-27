from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EcommercesConfig(AppConfig):
    name = "api.ecommerces"
    verbose_name = _("Ecommerces")

    def ready(self):
        try:
            import api.eccomerces.signals  # noqa F401
        except ImportError:
            pass
