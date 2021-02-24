from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Clothe, KindOfClothe, Manufacturer


@admin.register(KindOfClothe)
class KindOfClotheAdmin(admin.ModelAdmin):
    pass


@admin.register(Clothe)
class ClotheAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass
