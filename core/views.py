from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from django.http import HttpResponse
from datetime import timedelta
from .services.export import export_to_excel, export_to_pdf, get_export_filename

from .models import (
    RawMaterial, DailyConsumption, ProductType, DailyProduction,
    Customer, PurchaseOrder, PurchaseOrderItem, PurchaseOrderUpdate
)
from .forms import (
    RawMaterialForm, DailyConsumptionForm, ProductTypeForm, DailyProductionForm,
    CustomerForm, PurchaseOrderForm, PurchaseOrderItemFormSet, PurchaseOrderUpdateForm
)


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

    # Get recent consumption records and check if materials exist
    recent_consumptions = DailyConsumption.objects.select_related('raw_material').order_by('-created_at')[:10]
    materials_exist = RawMaterial.objects.exists()

    return render(request, 'core/consumption/form.html', {
        'form': form,
        'title': 'Record Consumption',
        'button_text': 'Save & Continue',
        'recent_records': recent_consumptions,
        'materials_exist': materials_exist,
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
    from itertools import groupby
    from operator import attrgetter

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

    # Order by date descending
    productions = productions.order_by('-date', '-created_at')

    # Group productions by date
    productions_by_day = []
    for date, group in groupby(productions, key=attrgetter('date')):
        productions_by_day.append({
            'date': date,
            'productions': list(group)
        })

    product_types = ProductType.objects.all().order_by('name')

    context = {
        'productions_by_day': productions_by_day,
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

    # Get recent production records and check if products exist
    recent_productions = DailyProduction.objects.select_related('product_type').order_by('-created_at')[:10]
    products_exist = ProductType.objects.exists()

    return render(request, 'core/production/form.html', {
        'form': form,
        'title': 'Record Production',
        'button_text': 'Save & Continue',
        'recent_records': recent_productions,
        'products_exist': products_exist,
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


# ===== CUSTOMER VIEWS =====

@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all().order_by('name')
    search = request.GET.get('search', '')

    if search:
        customers = customers.filter(name__icontains=search)

    context = {
        'customers': customers,
        'search': search,
    }
    return render(request, 'core/customers/list.html', context)


@login_required
def customer_create(request):
    """Create a new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'core/customers/form.html', {
        'form': form,
        'title': 'Add Customer',
        'button_text': 'Add Customer'
    })


@login_required
def customer_detail(request, pk):
    """View customer details and their orders"""
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.purchase_orders.all().order_by('-created_at')

    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'core/customers/detail.html', context)


@login_required
def customer_edit(request, pk):
    """Edit an existing customer"""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'core/customers/form.html', {
        'form': form,
        'title': 'Edit Customer',
        'button_text': 'Save Changes',
        'object': customer
    })


@login_required
def customer_delete(request, pk):
    """Delete a customer"""
    customer = get_object_or_404(Customer, pk=pk)

    if customer.purchase_orders.exists():
        messages.error(request, 'Cannot delete customer with existing orders.')
        return redirect('customer_detail', pk=customer.pk)

    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f'Customer "{name}" deleted successfully.')
        return redirect('customer_list')

    return render(request, 'core/confirm_delete.html', {
        'object': customer,
        'object_type': 'Customer'
    })


# ===== PURCHASE ORDER VIEWS =====

@login_required
def purchase_order_list(request):
    """List all purchase orders"""
    orders = PurchaseOrder.objects.select_related('customer').all()

    # Filter by status
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)

    # Filter by customer
    customer_id = request.GET.get('customer', '')
    if customer_id:
        orders = orders.filter(customer_id=customer_id)

    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)

    customers = Customer.objects.all().order_by('name')

    context = {
        'orders': orders,
        'status': status,
        'customer_id': customer_id,
        'date_from': date_from,
        'date_to': date_to,
        'customers': customers,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
    }
    return render(request, 'core/orders/list.html', context)


@login_required
def purchase_order_create(request):
    """Create a new purchase order"""
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            messages.success(request, 'Purchase order created successfully.')
            return redirect('purchase_order_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()

    # Get recent orders and check if customers/products exist
    recent_orders = PurchaseOrder.objects.select_related('customer').order_by('-created_at')[:10]
    customers_exist = Customer.objects.exists()
    products_exist = ProductType.objects.exists()

    return render(request, 'core/orders/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Purchase Order',
        'button_text': 'Create Order',
        'recent_records': recent_orders,
        'customers_exist': customers_exist,
        'products_exist': products_exist,
    })


@login_required
def purchase_order_detail(request, pk):
    """View purchase order details"""
    order = get_object_or_404(PurchaseOrder.objects.select_related('customer').prefetch_related('items', 'updates'), pk=pk)

    context = {
        'order': order,
        'items': order.items.all(),
        'updates': order.updates.all().order_by('-created_at'),
    }
    return render(request, 'core/orders/detail.html', context)


@login_required
def purchase_order_add_update(request, pk):
    """Add an update/delivery to a purchase order"""
    order = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        form = PurchaseOrderUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.purchase_order = order
            update.save()

            # Auto-update order status
            order.update_status_based_on_fulfillment()

            messages.success(request, 'Update added successfully.')
            return redirect('purchase_order_detail', pk=order.pk)
    else:
        form = PurchaseOrderUpdateForm()

    context = {
        'form': form,
        'order': order,
        'title': 'Add Delivery Update',
        'button_text': 'Add Update'
    }
    return render(request, 'core/orders/update_form.html', context)


@login_required
def purchase_order_change_status(request, pk):
    """Change purchase order status"""
    order = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(PurchaseOrder.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status changed to {order.get_status_display()}.')
            return redirect('purchase_order_detail', pk=order.pk)

    return render(request, 'core/orders/change_status.html', {
        'order': order,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
    })


@login_required
def purchase_order_delete(request, pk):
    """Delete a purchase order"""
    order = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        po_number = order.po_number
        order.delete()
        messages.success(request, f'Order {po_number} deleted successfully.')
        return redirect('purchase_order_list')

    return render(request, 'core/confirm_delete.html', {
        'object': order,
        'object_type': 'Purchase Order'
    })


# ===== EXPORT VIEWS =====

@login_required
def export_raw_materials_excel(request):
    """Export raw materials to Excel"""
    materials = RawMaterial.objects.all().order_by('category', 'name')

    data = []
    for material in materials:
        data.append({
            'Name': material.name,
            'Category': material.get_category_display(),
            'Unit': material.unit,
        })

    export_data = {
        'title': 'Raw Materials Library',
        'sheet_name': 'Raw Materials',
        'data': data,
        'summary': {'Total Materials': len(data)}
    }

    headers = ['Name', 'Category', 'Unit']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("raw_materials", "excel")}.xlsx"'
    return response


@login_required
def export_raw_materials_pdf(request):
    """Export raw materials to PDF"""
    materials = RawMaterial.objects.all().order_by('category', 'name')

    data = []
    for material in materials:
        data.append({
            'Name': material.name,
            'Category': material.get_category_display(),
            'Unit': material.unit,
        })

    export_data = {
        'title': 'Raw Materials Library',
        'data': data,
        'summary': {'Total Materials': len(data)}
    }

    headers = ['Name', 'Category', 'Unit']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("raw_materials", "pdf")}.pdf"'
    return response


@login_required
def export_consumption_excel(request):
    """Export consumption history to Excel"""
    consumption = DailyConsumption.objects.all().select_related('raw_material').order_by('-date')

    data = []
    total_qty = 0
    for record in consumption:
        data.append({
            'Date': record.date.strftime('%Y-%m-%d'),
            'Material': record.raw_material.name,
            'Category': record.raw_material.get_category_display(),
            'Quantity': str(record.quantity),
            'Unit': record.raw_material.unit,
        })
        total_qty += record.quantity

    export_data = {
        'title': 'Consumption History',
        'sheet_name': 'Consumption',
        'data': data,
        'summary': {'Total Records': len(data), 'Date Range': f'{consumption.last().date if consumption else "N/A"} to {consumption.first().date if consumption else "N/A"}'}
    }

    headers = ['Date', 'Material', 'Category', 'Quantity', 'Unit']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("consumption", "excel")}.xlsx"'
    return response


@login_required
def export_consumption_pdf(request):
    """Export consumption history to PDF"""
    consumption = DailyConsumption.objects.all().select_related('raw_material').order_by('-date')

    data = []
    for record in consumption:
        data.append({
            'Date': record.date.strftime('%Y-%m-%d'),
            'Material': record.raw_material.name,
            'Category': record.raw_material.get_category_display(),
            'Quantity': str(record.quantity),
            'Unit': record.raw_material.unit,
        })

    export_data = {
        'title': 'Consumption History',
        'data': data,
        'summary': {'Total Records': len(data)}
    }

    headers = ['Date', 'Material', 'Category', 'Quantity', 'Unit']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("consumption", "pdf")}.pdf"'
    return response


@login_required
def export_products_excel(request):
    """Export product types to Excel"""
    products = ProductType.objects.all().order_by('name')

    data = []
    for product in products:
        data.append({
            'Name': product.name,
            'Description': product.description or '',
        })

    export_data = {
        'title': 'Product Types',
        'sheet_name': 'Products',
        'data': data,
        'summary': {'Total Products': len(data)}
    }

    headers = ['Name', 'Description']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("products", "excel")}.xlsx"'
    return response


@login_required
def export_products_pdf(request):
    """Export product types to PDF"""
    products = ProductType.objects.all().order_by('name')

    data = []
    for product in products:
        data.append({
            'Name': product.name,
            'Description': product.description or '',
        })

    export_data = {
        'title': 'Product Types',
        'data': data,
        'summary': {'Total Products': len(data)}
    }

    headers = ['Name', 'Description']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("products", "pdf")}.pdf"'
    return response


@login_required
def export_production_excel(request):
    """Export production history to Excel"""
    production = DailyProduction.objects.all().select_related('product_type').order_by('-date')

    data = []
    for record in production:
        data.append({
            'Date': record.date.strftime('%Y-%m-%d'),
            'Product': record.product_type.name,
            'Quantity': str(record.quantity),
            'Contents': record.contents_description or '',
        })

    export_data = {
        'title': 'Production History',
        'sheet_name': 'Production',
        'data': data,
        'summary': {'Total Records': len(data)}
    }

    headers = ['Date', 'Product', 'Quantity', 'Contents']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("production", "excel")}.xlsx"'
    return response


@login_required
def export_production_pdf(request):
    """Export production history to PDF"""
    production = DailyProduction.objects.all().select_related('product_type').order_by('-date')

    data = []
    for record in production:
        data.append({
            'Date': record.date.strftime('%Y-%m-%d'),
            'Product': record.product_type.name,
            'Quantity': str(record.quantity),
            'Contents': record.contents_description or '',
        })

    export_data = {
        'title': 'Production History',
        'data': data,
        'summary': {'Total Records': len(data)}
    }

    headers = ['Date', 'Product', 'Quantity', 'Contents']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("production", "pdf")}.pdf"'
    return response


@login_required
def export_customers_excel(request):
    """Export customers to Excel"""
    customers = Customer.objects.all().order_by('name')

    data = []
    for customer in customers:
        order_count = customer.purchase_orders.count()
        data.append({
            'Name': customer.name,
            'Contact': customer.contact_info or '',
            'Orders': str(order_count),
        })

    export_data = {
        'title': 'Customers',
        'sheet_name': 'Customers',
        'data': data,
        'summary': {'Total Customers': len(data)}
    }

    headers = ['Name', 'Contact', 'Orders']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("customers", "excel")}.xlsx"'
    return response


@login_required
def export_customers_pdf(request):
    """Export customers to PDF"""
    customers = Customer.objects.all().order_by('name')

    data = []
    for customer in customers:
        order_count = customer.purchase_orders.count()
        data.append({
            'Name': customer.name,
            'Contact': customer.contact_info or '',
            'Orders': str(order_count),
        })

    export_data = {
        'title': 'Customers',
        'data': data,
        'summary': {'Total Customers': len(data)}
    }

    headers = ['Name', 'Contact', 'Orders']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("customers", "pdf")}.pdf"'
    return response


@login_required
def export_orders_excel(request):
    """Export purchase orders to Excel"""
    orders = PurchaseOrder.objects.all().select_related('customer').order_by('-created_at')

    data = []
    for order in orders:
        item_count = order.items.count()
        data.append({
            'PO Number': order.po_number,
            'Customer': order.customer.name,
            'Status': order.get_status_display(),
            'Items': str(item_count),
            'Progress': f"{order.overall_progress:.0f}%",
            'Created': order.created_at.strftime('%Y-%m-%d'),
        })

    export_data = {
        'title': 'Purchase Orders',
        'sheet_name': 'Orders',
        'data': data,
        'summary': {'Total Orders': len(data)}
    }

    headers = ['PO Number', 'Customer', 'Status', 'Items', 'Progress', 'Created']
    excel_file = export_to_excel(export_data, headers)

    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("orders", "excel")}.xlsx"'
    return response


@login_required
def export_orders_pdf(request):
    """Export purchase orders to PDF"""
    orders = PurchaseOrder.objects.all().select_related('customer').order_by('-created_at')

    data = []
    for order in orders:
        item_count = order.items.count()
        data.append({
            'PO Number': order.po_number,
            'Customer': order.customer.name,
            'Status': order.get_status_display(),
            'Items': str(item_count),
            'Progress': f"{order.overall_progress:.0f}%",
            'Created': order.created_at.strftime('%Y-%m-%d'),
        })

    export_data = {
        'title': 'Purchase Orders',
        'data': data,
        'summary': {'Total Orders': len(data)}
    }

    headers = ['PO Number', 'Customer', 'Status', 'Items', 'Progress', 'Created']
    pdf_file = export_to_pdf(export_data, headers)

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{get_export_filename("orders", "pdf")}.pdf"'
    return response
