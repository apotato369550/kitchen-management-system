from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta

from .models import RawMaterial, DailyConsumption, ProductType, DailyProduction
from .forms import RawMaterialForm, DailyConsumptionForm, ProductTypeForm, DailyProductionForm


@login_required
def dashboard(request):
    """Main dashboard view with today's summary"""
    today = timezone.now().date()

    # Get today's consumption and production counts
    today_consumption_count = DailyConsumption.objects.filter(date=today).count()
    today_production_count = DailyProduction.objects.filter(date=today).count()

    # Get recent activity (last 7 days)
    last_7_days = today - timedelta(days=7)
    recent_consumptions = DailyConsumption.objects.filter(date__gte=last_7_days).count()
    recent_productions = DailyProduction.objects.filter(date__gte=last_7_days).count()

    context = {
        'user': request.user,
        'today': today,
        'today_consumption_count': today_consumption_count,
        'today_production_count': today_production_count,
        'recent_consumptions': recent_consumptions,
        'recent_productions': recent_productions,
    }
    return render(request, 'core/dashboard.html', context)


# ===== RAW MATERIALS VIEWS =====

@login_required
def raw_material_list(request):
    """List all raw materials"""
    materials = RawMaterial.objects.all().order_by('category', 'name')
    category_filter = request.GET.get('category', '')

    if category_filter:
        materials = materials.filter(category=category_filter)

    context = {
        'materials': materials,
        'category_choices': RawMaterial.CATEGORY_CHOICES,
        'selected_category': category_filter,
    }
    return render(request, 'core/raw_materials/list.html', context)


@login_required
def raw_material_create(request):
    """Create a new raw material"""
    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Raw material added successfully.')
            return redirect('raw_material_list')
    else:
        form = RawMaterialForm()

    return render(request, 'core/raw_materials/form.html', {
        'form': form,
        'title': 'Add Raw Material',
        'button_text': 'Add Material'
    })


@login_required
def raw_material_edit(request, pk):
    """Edit an existing raw material"""
    material = get_object_or_404(RawMaterial, pk=pk)

    if request.method == 'POST':
        form = RawMaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Raw material updated successfully.')
            return redirect('raw_material_list')
    else:
        form = RawMaterialForm(instance=material)

    return render(request, 'core/raw_materials/form.html', {
        'form': form,
        'title': 'Edit Raw Material',
        'button_text': 'Save Changes',
        'object': material
    })


@login_required
def raw_material_delete(request, pk):
    """Delete a raw material"""
    material = get_object_or_404(RawMaterial, pk=pk)

    if request.method == 'POST':
        name = material.name
        material.delete()
        messages.success(request, f'Raw material "{name}" deleted successfully.')
        return redirect('raw_material_list')

    return render(request, 'core/confirm_delete.html', {
        'object': material,
        'object_type': 'Raw Material'
    })


# ===== DAILY CONSUMPTION VIEWS =====

@login_required
def consumption_history(request):
    """View consumption history"""
    consumptions = DailyConsumption.objects.select_related('raw_material').all()

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    category_filter = request.GET.get('category', '')

    if date_from:
        consumptions = consumptions.filter(date__gte=date_from)
    if date_to:
        consumptions = consumptions.filter(date__lte=date_to)
    if category_filter:
        consumptions = consumptions.filter(raw_material__category=category_filter)

    context = {
        'consumptions': consumptions,
        'date_from': date_from,
        'date_to': date_to,
        'category_choices': RawMaterial.CATEGORY_CHOICES,
        'selected_category': category_filter,
    }
    return render(request, 'core/consumption/list.html', context)


@login_required
def consumption_create(request):
    """Add a new consumption entry"""
    if request.method == 'POST':
        form = DailyConsumptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consumption recorded successfully.')

            # Check if user wants to add another
            if request.POST.get('add_another'):
                return redirect('consumption_create')
            return redirect('consumption_history')
    else:
        form = DailyConsumptionForm()

    return render(request, 'core/consumption/form.html', {
        'form': form,
        'title': 'Record Consumption',
        'button_text': 'Save & Continue'
    })


@login_required
def consumption_delete(request, pk):
    """Delete a consumption entry"""
    consumption = get_object_or_404(DailyConsumption, pk=pk)

    if request.method == 'POST':
        material = consumption.raw_material.name
        date = consumption.date
        consumption.delete()
        messages.success(request, f'Consumption entry deleted.')
        return redirect('consumption_history')

    return render(request, 'core/confirm_delete.html', {
        'object': consumption,
        'object_type': 'Consumption Entry'
    })


# ===== PRODUCT TYPES VIEWS =====

@login_required
def product_type_list(request):
    """List all product types"""
    products = ProductType.objects.all().order_by('name')

    context = {'products': products}
    return render(request, 'core/product_types/list.html', context)


@login_required
def product_type_create(request):
    """Create a new product type"""
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product type added successfully.')
            return redirect('product_type_list')
    else:
        form = ProductTypeForm()

    return render(request, 'core/product_types/form.html', {
        'form': form,
        'title': 'Add Product Type',
        'button_text': 'Add Product'
    })


@login_required
def product_type_edit(request, pk):
    """Edit an existing product type"""
    product = get_object_or_404(ProductType, pk=pk)

    if request.method == 'POST':
        form = ProductTypeForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product type updated successfully.')
            return redirect('product_type_list')
    else:
        form = ProductTypeForm(instance=product)

    return render(request, 'core/product_types/form.html', {
        'form': form,
        'title': 'Edit Product Type',
        'button_text': 'Save Changes',
        'object': product
    })


@login_required
def product_type_delete(request, pk):
    """Delete a product type"""
    product = get_object_or_404(ProductType, pk=pk)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product type "{name}" deleted successfully.')
        return redirect('product_type_list')

    return render(request, 'core/confirm_delete.html', {
        'object': product,
        'object_type': 'Product Type'
    })


# ===== DAILY PRODUCTION VIEWS =====

@login_required
def production_history(request):
    """View production history"""
    productions = DailyProduction.objects.select_related('product_type').all()

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    product_filter = request.GET.get('product', '')

    if date_from:
        productions = productions.filter(date__gte=date_from)
    if date_to:
        productions = productions.filter(date__lte=date_to)
    if product_filter:
        productions = productions.filter(product_type__id=product_filter)

    product_types = ProductType.objects.all().order_by('name')

    context = {
        'productions': productions,
        'date_from': date_from,
        'date_to': date_to,
        'product_types': product_types,
        'selected_product': product_filter,
    }
    return render(request, 'core/production/list.html', context)


@login_required
def production_create(request):
    """Add a new production entry"""
    if request.method == 'POST':
        form = DailyProductionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Production recorded successfully.')

            # Check if user wants to add another
            if request.POST.get('add_another'):
                return redirect('production_create')
            return redirect('production_history')
    else:
        form = DailyProductionForm()

    return render(request, 'core/production/form.html', {
        'form': form,
        'title': 'Record Production',
        'button_text': 'Save & Continue'
    })


@login_required
def production_delete(request, pk):
    """Delete a production entry"""
    production = get_object_or_404(DailyProduction, pk=pk)

    if request.method == 'POST':
        product = production.product_type.name
        date = production.date
        production.delete()
        messages.success(request, f'Production entry deleted.')
        return redirect('production_history')

    return render(request, 'core/confirm_delete.html', {
        'object': production,
        'object_type': 'Production Entry'
    })
