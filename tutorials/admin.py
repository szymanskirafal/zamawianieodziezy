from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Tutorial

class TutorialAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Tutorial, TutorialAdmin)
