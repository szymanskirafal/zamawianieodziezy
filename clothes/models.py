from django.db import models

from django.utils.timezone import localdate
from django.utils.translation import ugettext_lazy as _

import datetime

from orders.models import Order
from employees.models import Employee, Position


class Manufacturer(models.Model):
    name = models.CharField(_('Nazwa'), max_length = 150, unique = True)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Producent'
        verbose_name_plural = 'Producenci'

    def __str__(self):
        return self.name


class KindOfClothe(models.Model):
    name = models.CharField(_('Nazwa'), max_length = 150, unique = True)
    description = models.CharField(_('Opis'), max_length = 300, blank = True)
    months_to_exchange = models.PositiveSmallIntegerField(_('Czasokres wymiany w miesiącach'),)
    available_for = models.ManyToManyField(
        Position,
        verbose_name = _('Dostęopne dla'),
        )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete = models.CASCADE,
        verbose_name = _('Producent'),
        )

    class Meta:
        verbose_name = 'Rodzaj Ubrania'
        verbose_name_plural = 'Rodzaje ubrań'

    def __str__(self):
        names = set(
           position.name
           for position
           in self.available_for.all()
           )
        positions = ', '.join(names)
        return self.name + ', wymiana co ' + str(self.months_to_exchange) + ', przysluguje: ' + positions


class Clothe(models.Model):
    kind = models.ForeignKey(
        KindOfClothe,
        on_delete = models.CASCADE,
        related_name = 'chosen',
        verbose_name = _('Rodzaj'),
        )
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name = 'clothes_in_order',
        verbose_name = _('Zamówienie'),
        )
    employee = models.ForeignKey(
        Employee,
        on_delete = models.CASCADE,
        related_name = 'clothes',
        verbose_name = _('Pracownik'),
        )
    prepared_to_order = models.BooleanField(null = False, blank = False, default = False)
    ordered = models.DateField(null = True, blank = True)
    received = models.DateField(null = True, blank = True)
    delivered_ok = models.BooleanField(null = False, blank = False, default = False)
    delivered_with_defects = models.BooleanField(null = False, blank = False, default = False)
    not_delivered = models.BooleanField(null = False, blank = False, default = False)
    owned = models.DateField(null = True, blank = True)
    in_use = models.BooleanField(null = False, blank = False, default = False)
    destroyed = models.DateField(null = True, blank = True)

    class Meta:
        ordering = ['-ordered']
        verbose_name = 'Ubranie'
        verbose_name_plural = 'Ubrania pracowników'

    def __str__(self):
        return str(self.kind) + ' ' + str(self.employee)

    def can_be_ordered_again(self):
        today = localdate()
        if self.ordered == None:
            return True
        else:
            ordered = self.ordered
            days = self.kind.months_to_exchange * 30
            time_to_order_again = datetime.timedelta(days = days)
            if  ordered + time_to_order_again < today:
                return True
            else:
                return False

    def time_to_order_again(self):
        ordered = self.ordered
        days = self.kind.months_to_exchange * 30
        time_to_order_again = datetime.timedelta(days = days)
        date_to_order_again = ordered + time_to_order_again
        return date_to_order_again
