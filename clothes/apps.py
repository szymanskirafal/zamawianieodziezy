from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _

class ClothesConfig(AppConfig):
    name = 'clothes'
    verbose_name = _('Ubrania')
