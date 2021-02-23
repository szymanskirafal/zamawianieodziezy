from django.forms import HiddenInput, ModelForm

from .models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'job',
            'work_place',
            'sex',
            'name',
            'surname',
            'height',
            'colar',
            'width_waist',
            'body_size',
            'shoe_size',
        ]
