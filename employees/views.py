from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.views import generic

from clothes.models import KindOfClothe, Clothe
from orders.models import Order

from .forms import EmployeeForm
from .models import Employee


class EmployeeCreateView(generic.CreateView):
    form_class = EmployeeForm
    model = Employee
    success_url = reverse_lazy('employees:employees')
    template_name = 'employees/add.html'


class EmployeeUpdateView(generic.UpdateView):
    context_object_name = 'employee'
    form_class = EmployeeForm
    model = Employee
    success_url = reverse_lazy('employees:employees')
    template_name = 'employees/update.html'


class EmployeeDetailView(generic.DetailView):
    context_object_name = 'employee'
    model = Employee
    template_name = 'employees/employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kinds_that_can_be_ordered'] = self.get_kinds_that_can_be_ordered()
        context['kinds_prepared_to_order'] = self.get_kinds_prepared_to_order()
        context['kinds_that_can_not_be_ordered_yet'] = self.get_kinds_that_can_not_be_ordered_yet()
        return context

    def get_kinds_not_ordered_yet_but_availalble(self):

        kinds_available = KindOfClothe.objects.all().filter(
            (Q(available_for=self.object.job.position_1) | Q(available_for=self.object.job.position_2))
            )

        kinds_ordered = set(
            clothe.kind
            for clothe
            in self.object.clothes.all()
            )

        return set(
            kind
            for kind
            in kinds_available
            if kind not in kinds_ordered
            )

    def get_kinds_that_can_be_ordered_again_but_not_prepared_to_order(self):
        clothes = self.object.clothes.all()
        clothes = clothes.filter(prepared_to_order = False)
        return set(
            clothe.kind
            for clothe
            in clothes
            if clothe.can_be_ordered_again == True
            )

    def get_kinds_that_can_be_ordered(self):
        return set(
            kind
            for kind
            in (self.get_kinds_that_can_be_ordered_again_but_not_prepared_to_order() | self.get_kinds_not_ordered_yet_but_availalble())
            )

    def get_kinds_that_can_not_be_ordered_yet(self):
        return set(
            clothe.kind
            for clothe
            in self.object.clothes.all()
            if clothe.can_be_ordered_again == False
            )

    def get_kinds_prepared_to_order(self):
        clothes = self.object.clothes.all()
        clothes = clothes.filter(prepared_to_order = True)
        return set(
            clothe.kind
            for clothe
            in clothes
            )


class EmployeesListView(generic.ListView):
    context_object_name = 'employees'
    work_place = None
    model = Employee
    template_name = 'employees/employees.html'

    def get_work_place(self):
        if self.work_place:
            return self.work_place
        else:
            self.work_place = self.request.user.manager.work_place
            return self.work_place

    def get_order_not_sent(self):
        try:
            order = Order.objects.all().filter(manager = self.request.user.manager).filter(during_composing = True)
        except ObjectDoesNotExist:
            order = None
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_place'] = self.get_work_place()
        context['order_not_sent'] = self.get_order_not_sent()
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(
            work_place = self.get_work_place()
            )
        return queryset
