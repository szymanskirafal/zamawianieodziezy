from django.db import models
from django.utils.translation import ugettext_lazy as _

from embed_video.fields import EmbedVideoField

class Tutorial(models.Model):
    title = models.CharField(_('Tytuł'), max_length = 40, unique = True)
    video = EmbedVideoField()

    def __str__(self):
        return 'Tutorial: ' + self.title
