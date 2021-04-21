from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.views import generic

from clothes.models import Clothe
from employees.models import Employee
from orders.forms import OrderSendToManufacturerForm
from orders.models import Order

class SupervisorPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        try:
            test =  self.request.user.supervisor
        except ObjectDoesNotExist:
            test = False
        return test

class SupervisorClotheDeleteView(generic.DeleteView):
    context_object_name = 'clothe'
    model = Clothe
    template_name = "clothes/delete.html"
    success_url = reverse_lazy('supervisor:dashboard')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        order = self.object.order
        self.object.delete()
        if not order.clothes_in_order.exists():
            order.delete()
        return HttpResponseRedirect(success_url)


class SupervisorOrderDetailView(
    LoginRequiredMixin,
    SupervisorPassesTestMixin,
    generic.DetailView,
    ):

    context_object_name = 'order'
    model = Order
    template_name = 'supervisor/order.html'

    def get_clothes(self):
        clothes = Clothe.objects.all()
        clothes = clothes.filter(order = self.get_object())
        clothes = clothes.select_related('employee', 'kind', )
        return clothes.values(
            'id',
            'employee__id',
            'employee__name',
            'employee__surname',
            'kind__name',
            )

    def get_employees_with_prefetched(self):
        employees = Employee.objects.all()
        employees = employees.filter(work_place = self.get_work_place())
        employees = employees.prefetch_related('clothes', )
        return employees.values(
            'id',
            'name',
            'clothes__kind__name',
            'clothes__prepared_to_order',
            'clothes__ordered',
            'clothes__received',
            'clothes__delivered_ok',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clothes'] = self.get_clothes()
        context['employees_with_prefetched'] = self.get_employees_with_prefetched()
        return context

    def get_work_place(self):
        return self.get_object().place_of_delivery


class SupervisorOrderUpdateView(
    LoginRequiredMixin,
    SupervisorPassesTestMixin,
    generic.UpdateView,
    ):

    context_object_name = 'order'
    form_class = OrderSendToManufacturerForm
    model = Order
    success_url = reverse_lazy('supervisor:sent')
    template_name = 'supervisor/send.html'

    def form_valid(self, form):
        form.instance.approved_by_supervisor = True
        form.instance.sent_to_manufacturer = True
        form.instance.date_of_sending_to_manufacturer = localdate()
        from_email =  getattr(settings, "DEFAULT_FROM_EMAIL")
        to =  getattr(settings, "DEFAULT_TO_EMAIL")
        #fake_manufacturer_email =  getattr(settings, "FAKE_MANUFACTURER_EMAIL")
        #fake_supervisor_email = getattr(settings, "FAKE_SUPERVISOR_EMAIL")
        #manufaturer_email = fake_manufacturer_email
        #supervisor_email = fake_supervisor_email
        email = EmailMessage(
            subject = 'Zamówienie odzieży roboczej',
            body = 'W aplikacji jest nowe zamówienie',
            from_email = from_email,
            to = [to, ],
        )
        email.send()
        return super().form_valid(form)


class SupervisorOrderSentTemplateView(
    LoginRequiredMixin,
    SupervisorPassesTestMixin,
    generic.TemplateView,
    ):

    template_name = "supervisor/sent.html"


class SupervisorDashboardTemplateView(
    LoginRequiredMixin,
    SupervisorPassesTestMixin,
    generic.TemplateView,
    ):

    template_name = "supervisor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        context['orders_not_approved'] = orders.filter(approved_by_supervisor = False)
        context['orders_sent_to_manufacturer'] = orders.filter(sent_to_manufacturer = True)
        context['orders_received_from_manufacturer'] = orders.filter(received_from_manufacturer = True)
        return context
