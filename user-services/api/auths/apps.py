from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthsConfig(AppConfig):
    name = "api.auths"
    verbose_name = _("Auths")

    def ready(self):
        try:
            import api.auths.signals  # noqa F401
        except ImportError:
            pass
