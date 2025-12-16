from django import forms
from django.forms import inlineformset_factory
from .models import (
    RawMaterial, DailyConsumption, ProductType, DailyProduction,
    Customer, PurchaseOrder, PurchaseOrderItem, PurchaseOrderUpdate
)


class RawMaterialForm(forms.ModelForm):
    """Form for creating and editing raw materials"""

    class Meta:
        model = RawMaterial
        fields = ['name', 'category', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Chicken Breast'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., grams, pieces, heads'
            }),
        }


class DailyConsumptionForm(forms.ModelForm):
    """Form for recording daily consumption of raw materials"""

    class Meta:
        model = DailyConsumption
        fields = ['date', 'raw_material', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'raw_material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': 'Enter quantity'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('date'):
            from django.utils import timezone
            self.initial['date'] = timezone.now().date()


class ProductTypeForm(forms.ModelForm):
    """Form for creating and editing product types"""

    class Meta:
        model = ProductType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Food Pack, Platter, Bilao'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }


class DailyProductionForm(forms.ModelForm):
    """Form for recording daily production output"""

    class Meta:
        model = DailyProduction
        fields = ['date', 'product_type', 'quantity', 'contents_description']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter quantity produced'
            }),
            'contents_description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Describe contents (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('date'):
            from django.utils import timezone
            self.initial['date'] = timezone.now().date()


class CustomerForm(forms.ModelForm):
    """Form for creating and editing customers"""

    class Meta:
        model = Customer
        fields = ['name', 'contact_info']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Customer name'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone, email, or address'
            }),
        }


class PurchaseOrderForm(forms.ModelForm):
    """Form for creating purchase orders"""

    class Meta:
        model = PurchaseOrder
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }


class PurchaseOrderItemForm(forms.ModelForm):
    """Form for purchase order line items"""

    class Meta:
        model = PurchaseOrderItem
        fields = ['product_type', 'quantity_ordered']
        widgets = {
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity_ordered': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Quantity',
                'min': '1'
            }),
        }


# Formset for inline editing of purchase order items
PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    can_delete=True
)


class PurchaseOrderUpdateForm(forms.ModelForm):
    """Form for adding updates/deliveries to purchase orders"""

    class Meta:
        model = PurchaseOrderUpdate
        fields = ['note', 'quantity_delivered']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Add a note about this delivery or update'
            }),
            'quantity_delivered': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Quantity delivered (optional)',
                'min': '0',
                'step': '1'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity_delivered'].required = False
