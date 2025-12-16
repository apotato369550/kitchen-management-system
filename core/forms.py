from django import forms
from .models import RawMaterial, DailyConsumption, ProductType, DailyProduction


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
