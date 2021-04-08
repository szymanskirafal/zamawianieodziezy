from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class WorkPlace(models.Model):
    STATION = 'ST'
    BASE = 'BA'
    TYPE_OF_WORKPLACE = [
        (STATION, 'Stacja Paliw'),
        (BASE, 'Baza Magazynowa'),
        ]
    rodzaj = models.CharField(
        max_length = 2,
        choices = TYPE_OF_WORKPLACE,
        default = STATION,
        )
    name = models.CharField(_('Nazwa'), max_length = 150)
    street = models.CharField(_('Ulica'), max_length = 50)
    city = models.CharField(_('Miejscowość'), max_length = 50)
    postal_code = models.CharField(_('Kod pocztowy'), max_length = 8)
    phone = models.CharField(_('Telefon'), max_length = 13)
    email = models.EmailField(_('email'), )

    class Meta:
        verbose_name = 'Miejsce Pracy'
        verbose_name_plural = 'Miejsca Pracy'

    def __str__(self):
        return self.name + ', ' + self.city


class Position(models.Model):
    name = models.CharField(_('Nazwa'), max_length = 150)
    description = models.CharField(_('Opis'), blank = True, max_length = 300)

    class Meta:
        verbose_name = 'Stanowisko'
        verbose_name_plural = 'Stanowiska'

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
    name = models.CharField(_('Nazwa'), max_length = 150)
    position_1 = models.ForeignKey(
        Position,
        on_delete = models.CASCADE,
        related_name = 'first_position',
        verbose_name = _('stanowisko pierwsze'),
        )
    size_of_position_1 = models.DecimalField(
        _('wielkość etatu na stanowisku 1'),
        max_digits = 3,
        decimal_places = 2,
        )
    position_2 = models.ForeignKey(
        Position,
        null = True,
        blank = True,
        on_delete = models.CASCADE,
        related_name = 'second_position',
        verbose_name = _('stanowisko drugie'),
        )
    size_of_position_2 = models.DecimalField(
        _('wielkość etatu nastanowisku 2'),
        null = True,
        blank = True,
        max_digits = 3,
        decimal_places = 2,
        )

    class Meta:
        verbose_name = 'Etat'
        verbose_name_plural = 'Etaty'

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    WOMAN = 'W'
    MAN = 'M'
    SEX = [
        (WOMAN, 'Kobieta'),
        (MAN, 'Mężczyzna'),
        ]
    XL = 'XL'
    L = 'L'
    M = 'M'
    S = 'S'
    SIZE = [
        (XL, 'XL'),
        (L, 'L'),
        (M, 'M'),
        (S, 'S'),
        ]
    name = models.CharField(_('imię'), max_length = 15)
    surname = models.CharField(_('nazwisko'), max_length = 40)
    sex = models.CharField(_('płeć'), max_length = 1, choices = SEX,)
    height = models.PositiveSmallIntegerField(_('wzrost'), )
    colar = models.PositiveSmallIntegerField(_('kołnierzyk'), )
    chest = models.PositiveSmallIntegerField(_('obwód klatki'), )
    width_waist = models.PositiveSmallIntegerField(_('szerokość w pasie'), )
    body_size = models.CharField(_('rozmiar'), max_length = 2, choices = SIZE,)
    shoe_size = models.PositiveSmallIntegerField(_('nr buta'), )

    class Meta:
        abstract = True


class Employee(Person):
    job = models.ForeignKey(
        Job,
        on_delete = models.CASCADE,
        verbose_name = _('praca'),
        )
    work_place = models.ForeignKey(
        WorkPlace,
        on_delete = models.CASCADE,
        verbose_name = _('miejsce pracy'),
        )

    class Meta:
        verbose_name = 'Pracownik'
        verbose_name_plural = 'Pracownicy'

    def __str__(self):
        return self.name + ' ' + self.surname  + ' - ' + str(self.job) + ' - ' + str(self.work_place)

    def get_absolut_url(self):
        return reverse('employees:employee', args=[str(self.id)])


class Manager(Person):
    #job = models.ForeignKey(
    #    Job,
    #    on_delete = models.CASCADE,
    #    verbose_name = _('praca'),
    #    )
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    work_place = models.ForeignKey(
        WorkPlace,
        on_delete = models.CASCADE,
        verbose_name = _('miejsce pracy'),
        )
    email = models.EmailField()

    class Meta:
        verbose_name = 'Kierownik'
        verbose_name_plural = 'Kierownicy'

    def __str__(self):
        return self.name + ' ' + self.surname + ' - ' + str(self.work_place)


class Supervisor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete = models.CASCADE,
        verbose_name = _('użytkownik'),
        )
    name = models.CharField(_('Imię i Nazwisko'), max_length = 50)
    email = models.EmailField(_('email'), )

    class Meta:
        verbose_name = 'Nadzorca'
        verbose_name_plural = 'Nadzorcy'

    def __str__(self):
        return self.name
