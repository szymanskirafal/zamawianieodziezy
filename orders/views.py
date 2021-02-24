from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.views import generic

from clothes.models import Clothe, KindOfClothe
from employees.models import Employee, Manager, Supervisor

from .forms import OrderSendToSupervisorUpdateForm
from .models import Order


class OrdersListView(generic.ListView):
    context_object_name = 'orders'
    model = Order
    template_name = "orders/orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_during_composing'] = self.queryset.filter(during_composing = True).exists()
        context['orders_sent_to_supervisor'] = self.queryset.filter(sent_to_supervisor = True).exists()
        context['orders_waiting_for_delivery'] = self.queryset.filter(sent_to_manufacturer = True).exists()
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        manager = Manager.objects.get(pk = self.request.user.manager.pk)
        self.queryset = Order.objects.all().filter(manager = manager)
        return self.queryset


class OrderNextOrSendTemplateView(generic.TemplateView):
    template_name = "orders/order-next-or-send.html"


class OrdersArchivedListView(generic.ListView):
    template_name = "orders/archived.html"


class OrdersPreparedTemplateView(generic.TemplateView):
    template_name = "orders/prepared.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_order()
        context['clothes'] = self.get_clothes()
        return context

    def get_order(self):
        orders = Order.objects.all()
        orders = orders.filter(
            manager = Manager.objects.get(pk = self.request.user.manager.pk)
            )
        orders = orders.select_related('place_of_delivery', )
        self.order = orders.get(during_composing = True)
        return self.order

    def get_clothes(self):
        clothes = Clothe.objects.all()
        clothes = clothes.filter(order = self.order)
        clothes = clothes.select_related('employee', 'kind', )
        return clothes.values(
            'id',
            'kind__name',
            'employee__name',
            'employee__surname',
            )


class OrderSendUpdateView(generic.UpdateView):
    form_class = OrderSendToSupervisorUpdateForm
    model = Order
    success_url = reverse_lazy('employees:employees')
    template_name = "orders/send-to-supervisor.html"

    def form_valid(self, form):
        form.instance.during_composing = False
        form.instance.composed = True
        form.instance.sent_to_supervisor = True
        form.instance.date_of_sending_to_supervisor = localdate()
        #supervisor = Supervisor.objects.first()
        #email = EmailMessage(
        #    subject = 'Zamówienie odzieży roboczej',
        #    body = 'W aplikacji jest nowe zamówienie',
        #    to = [supervisor.email],
        #    )
        #email.send()
        print('------ date ', form.instance.date_of_sending_to_supervisor)
        return super().form_valid(form)


class OrdersAtSupervisorListView(generic.ListView):
    context_object_name = 'orders'
    model = Order
    template_name = 'orders/at-supervisor.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        manager = Manager.objects.get(pk = self.request.user.manager.pk)
        queryset = Order.objects.all().filter(manager = manager)
        queryset = queryset.filter(sent_to_supervisor = True)
        queryset = queryset.filter(approved_by_supervisor = False)
        return queryset

class OrdersAtSupervisorDetailView(generic.DetailView):
    context_object_name = 'order'
    model = Order
    template_name = 'orders/at-supervisor-detail.html'

    def get_clothes(self):
        clothes = Clothe.objects.all()
        clothes = clothes.filter(order = self.get_object())
        clothes = clothes.select_related('employee', 'kind', )
        return clothes.values(
            'id',
            'kind__name',
            'employee__name',
            'employee__surname',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clothes'] = self.get_clothes()
        return context


class OrderSentToManufacturerListView(generic.ListView):
    context_object_name = 'orders'
    model = Order
    template_name = 'orders/sent-list.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        manager = Manager.objects.get(pk = self.request.user.manager.pk)
        queryset = Order.objects.all().filter(manager = manager)
        queryset = queryset.filter(sent_to_manufacturer = True)
        return queryset


class OrderSentDetailView(generic.DetailView):
    context_object_name = 'order'
    model = Order
    template_name = 'orders/sent-detail.html'
