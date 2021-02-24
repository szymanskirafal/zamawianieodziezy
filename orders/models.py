from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from employees.models import Manager, WorkPlace


class Order(models.Model):
    manager = models.ForeignKey(
        Manager,
        on_delete = models.CASCADE,
        verbose_name = _('manager'),
        )
    place_of_delivery = models.ForeignKey(
        WorkPlace,
        on_delete = models.CASCADE,
        verbose_name = _('place_of_delivery'),
        )
    during_composing = models.BooleanField(_('during_composing'), default = True)
    composed = models.BooleanField(_('composed'), default = False)
    sent_to_supervisor = models.BooleanField(_('sent_to_supervisor'), default = False)
    date_of_sending_to_supervisor = models.DateField(_('date_of_sending_to_supervisor'), null = True, blank = True)
    approved_by_supervisor = models.BooleanField(_('approved_by_supervisor'), default = False)
    sent_to_manufacturer = models.BooleanField(_('sent_to_manufacturer'), default = False)
    date_of_sending_to_manufacturer = models.DateField(_('date_of_sending_to_manufacturer'), null = True, blank = True)
    received_from_manufacturer = models.BooleanField(_('received_from_manufacturer'), default = False)
    date_of_receiving_from_manufacturer = models.DateField(_('date_of_receiving_from_manufacturer'), null = True, blank = True)

    class Meta:
        verbose_name = 'Zamówienia'
        verbose_name_plural = 'Zamówienia'

    def get_absolute_url(self):
        return reverse('orders:order', args=[str(self.id)])
