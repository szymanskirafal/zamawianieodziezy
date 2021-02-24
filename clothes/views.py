from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils.timezone import localdate

from employees.models import Employee
from orders.models import Order

from .forms import ClotheCreateForm, ClotheDeliveredForm
from .models import Clothe, KindOfClothe


class KindsOfClothesListView(generic.ListView):
    model = KindOfClothe
    template_name = "clothes/kinds.html"


class ClotheCreateView(generic.CreateView):
    form_class = ClotheCreateForm
    model = Clothe
    success_url = reverse_lazy('employees:employees')
    template_name = "clothes/clothe-create.html"

    def form_valid(self, form):
        form.instance.kind = KindOfClothe.objects.get(pk = self.kwargs['kind_pk'])
        manager = self.request.user.manager
        order, created = Order.objects.get_or_create(
            manager = manager,
            place_of_delivery = manager.work_place,
            during_composing = True,
            )
        form.instance.order = order
        form.instance.employee = Employee.objects.get(pk = self.kwargs['employee_pk'])
        form.instance.prepared_to_order = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(pk = self.kwargs['employee_pk'])
        context['kind'] = KindOfClothe.objects.get(pk = self.kwargs['kind_pk'])
        return context


class ClotheDeleteView(generic.DeleteView):
    context_object_name = 'clothe'
    model = Clothe
    template_name = "clothes/delete.html"
    success_url = '/orders/'

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


class ClotheDeliveredUpdateView(generic.UpdateView):
    context_object_name = 'clothe'
    form_class = ClotheDeliveredForm
    model = Clothe
    template_name = "clothes/delivered.html"

    def form_valid(self, form):
        form.instance.prepared_to_order = False
        form.instance.received = localdate()
        form.instance.delivered_ok = True
        form.instance.in_use = True
        print('--- ', form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:sent-detail', args = [self.object.order.pk])


class ClotheDeliveredWithDefectsUpdateView(generic.UpdateView):
    context_object_name = 'clothe'
    form_class = ClotheDeliveredForm
    model = Clothe
    template_name = "clothes/delivered-with-defects.html"

    def form_valid(self, form):
        form.instance.received = localdate()
        form.instance.delivered_ok = False
        form.instance.delivered_with_defects = True
        form.instance.in_use = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:sent-detail', args = [self.object.order.pk])


class ClotheNotDeliveredUpdateView(generic.UpdateView):
    context_object_name = 'clothe'
    form_class = ClotheDeliveredForm
    model = Clothe
    template_name = "clothes/not-delivered.html"

    def form_valid(self, form):
        form.instance.received = localdate()
        form.instance.delivered_ok = False
        form.instance.delivered_with_defects = False
        form.instance.not_delivered = True
        form.instance.in_use = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:sent-detail', args = [self.object.order.pk])


class KindTemplateView(generic.TemplateView):
    template_name = 'clothes/kind-template.html'
