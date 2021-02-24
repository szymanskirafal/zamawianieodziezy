from django.forms import HiddenInput, ModelForm

from .models import Clothe


class ClotheCreateForm(ModelForm):
    class Meta:
        model = Clothe
        fields = [
            'ordered',
            'received',
            'destroyed',
            ]
        widgets = {
            'ordered': HiddenInput,
            'received': HiddenInput,
            'destroyed': HiddenInput,
        }


class ClotheDeliveredForm(ModelForm):
    class Meta:
        model = Clothe
        fields = [
            'ordered',
            'received',
            'delivered_ok',
            'delivered_with_defects',
            'not_delivered',
            'in_use',
            ]
        widgets = {
            'ordered': HiddenInput,
            'received': HiddenInput,
            'delivered_ok': HiddenInput,
            'delivered_with_defects': HiddenInput,
            'not_delivered': HiddenInput,
            'in_use': HiddenInput,
        }
