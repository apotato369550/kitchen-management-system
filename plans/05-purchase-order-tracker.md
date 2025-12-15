# Purchase Order Tracker Plan

## Goal
Build a complete purchase order management system with customer tracking, order fulfillment (full or staggered), and update history.

## Features Overview

### 1. Customer Management
- Create and manage customer records
- Store customer name and contact information
- Link customers to their purchase orders

### 2. Purchase Order Management
- Create new purchase orders for customers
- Add multiple product line items to each order
- Track order status: Pending, In Progress, Completed, Cancelled
- View all orders with filtering and search

### 3. Order Fulfillment Tracking
- Track quantity ordered vs. quantity fulfilled per line item
- Support staggered fulfillment (partial deliveries)
- Update history log (comment-style updates)
- Record delivery quantities with timestamps

## Implementation Steps

### 1. Customer Management UI

#### Views Needed:
1. **Customer List** (`/customers/`)
   - Table of all customers
   - Columns: Name, Contact Info, Total Orders, Created Date
   - Search by name
   - Add new customer button

2. **Customer Detail** (`/customers/<uuid>/`)
   - Customer information
   - List of all purchase orders for this customer
   - Edit customer button
   - Create new order button

3. **Customer Form** (`/customers/add/`, `/customers/<uuid>/edit/`)
   - Name field (required)
   - Contact info field (optional)
   - Save/Cancel buttons

### 2. Purchase Order Management UI

#### Views Needed:
1. **Purchase Order List** (`/orders/`)
   - Card or table layout showing all orders
   - Display: PO Number, Customer, Status, Items Count, Created Date
   - Filter by: Status, Customer, Date Range
   - Color-coded status badges
   - Search functionality
   - "Create New Order" button

2. **Purchase Order Detail** (`/orders/<uuid>/`)
   - Order information header:
     - PO Number (e.g., PO-12345678)
     - Customer name (link to customer detail)
     - Status badge
     - Created/Updated timestamps

   - Line Items Table:
     - Product Type, Quantity Ordered, Quantity Fulfilled, Progress Bar
     - Show percentage fulfilled (e.g., "50/100 - 50%")

   - Fulfillment Actions:
     - "Add Delivery Update" button
     - "Mark as Completed" button (when fully fulfilled)
     - "Change Status" dropdown

   - Update History (comment-style):
     - List of all updates chronologically
     - Each update shows: timestamp, note, delivery quantity (if applicable)
     - Most recent at top

3. **Create Purchase Order** (`/orders/create/`)
   - Step 1: Select customer (dropdown with search)
   - Step 2: Add line items
     - Product type dropdown
     - Quantity input
     - "Add Item" button
     - Show added items in table below
     - Remove item option
   - Submit button
   - Initial status: Pending

4. **Add Delivery Update** (`/orders/<uuid>/update/`)
   - Modal or separate page
   - Fields:
     - Note/Comment (textarea, required)
     - Product type (if recording delivery)
     - Quantity delivered (optional, for staggered fulfillment)
   - Update fulfillment quantities automatically
   - Add to update history

### 3. URL Structure
```python
# core/urls.py (continued)
urlpatterns += [
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<uuid:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<uuid:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<uuid:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Purchase Orders
    path('orders/', views.purchase_order_list, name='purchase_order_list'),
    path('orders/create/', views.purchase_order_create, name='purchase_order_create'),
    path('orders/<uuid:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('orders/<uuid:pk>/edit/', views.purchase_order_edit, name='purchase_order_edit'),
    path('orders/<uuid:pk>/update/', views.purchase_order_add_update, name='purchase_order_add_update'),
    path('orders/<uuid:pk>/status/', views.purchase_order_change_status, name='purchase_order_change_status'),
    path('orders/<uuid:pk>/delete/', views.purchase_order_delete, name='purchase_order_delete'),
]
```

### 4. Forms Implementation

#### Customer Form:
```python
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-input'}),
        }
```

#### Purchase Order Form:
```python
class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }

# Inline formset for order items
PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    fields=['product_type', 'quantity_ordered'],
    extra=1,
    can_delete=True
)
```

#### Update Form:
```python
class PurchaseOrderUpdateForm(forms.ModelForm):
    # Optional: select which item was delivered
    item = forms.ModelChoiceField(
        queryset=None,  # Set in view
        required=False,
        label='Product Delivered (optional)'
    )

    class Meta:
        model = PurchaseOrderUpdate
        fields = ['note', 'quantity_delivered']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'quantity_delivered': forms.NumberInput(attrs={'class': 'form-input'}),
        }
```

### 5. Template Structure
```
core/templates/core/
├── customers/
│   ├── list.html                  # Customer list
│   ├── detail.html                # Customer detail with orders
│   └── form.html                  # Add/edit customer
└── orders/
    ├── list.html                  # Purchase order list
    ├── detail.html                # Purchase order detail
    ├── form.html                  # Create/edit order
    └── update_form.html           # Add update/delivery
```

### 6. Key Features Implementation

#### A. Progress Tracking
Calculate fulfillment progress per item:
```python
# In PurchaseOrderItem model
@property
def fulfillment_percentage(self):
    if self.quantity_ordered == 0:
        return 0
    return (self.quantity_fulfilled / self.quantity_ordered) * 100

@property
def is_fulfilled(self):
    return self.quantity_fulfilled >= self.quantity_ordered
```

Calculate overall order progress:
```python
# In PurchaseOrder model
@property
def overall_progress(self):
    items = self.items.all()
    if not items:
        return 0
    total_ordered = sum(item.quantity_ordered for item in items)
    total_fulfilled = sum(item.quantity_fulfilled for item in items)
    if total_ordered == 0:
        return 0
    return (total_fulfilled / total_ordered) * 100

@property
def is_fully_fulfilled(self):
    return all(item.is_fulfilled for item in self.items.all())
```

#### B. Status Management
Auto-update status based on fulfillment:
```python
def update_status_based_on_fulfillment(self):
    if self.is_fully_fulfilled:
        self.status = 'completed'
    elif self.overall_progress > 0:
        self.status = 'in_progress'
    else:
        self.status = 'pending'
    self.save()
```

#### C. Staggered Delivery Recording
When adding an update with quantity delivered:
```python
# In view
def add_delivery_update(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.purchase_order = order
            update.save()

            # Update item fulfillment if quantity was specified
            if update.quantity_delivered and form.cleaned_data.get('item'):
                item = form.cleaned_data['item']
                item.quantity_fulfilled += update.quantity_delivered
                item.save()

            # Auto-update order status
            order.update_status_based_on_fulfillment()

            messages.success(request, 'Update added successfully')
            return redirect('purchase_order_detail', pk=order.pk)
```

### 7. UI/UX Design

#### Status Color Coding:
- **Pending**: Gray/Blue
- **In Progress**: Yellow/Orange
- **Completed**: Green
- **Cancelled**: Red

#### Progress Bars:
Use Tailwind progress bars for visual fulfillment tracking:
```html
<div class="w-full bg-gray-200 rounded-full h-2.5">
    <div class="bg-blue-600 h-2.5 rounded-full" style="width: {{ item.fulfillment_percentage }}%"></div>
</div>
```

#### Order Cards:
On the order list page, use cards for better visual hierarchy:
- Customer name prominent
- Status badge in corner
- Quick stats (items, progress)
- Click to view details

### 8. Search & Filtering

#### Order List Filters:
- Status dropdown (All, Pending, In Progress, Completed, Cancelled)
- Customer search/filter
- Date range picker (created date)

#### Implementation:
```python
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()

    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    # Filter by customer
    customer_id = request.GET.get('customer')
    if customer_id:
        orders = orders.filter(customer_id=customer_id)

    # Date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        orders = orders.filter(created_at__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__lte=date_to)

    return render(request, 'core/orders/list.html', {'orders': orders})
```

### 9. Validation Rules
- Customer name is required
- Purchase order must have at least one line item
- Quantity ordered must be positive
- Quantity fulfilled cannot exceed quantity ordered
- Cannot delete customer with existing orders (prevent or cascade)
- Status transitions should be logical (optional: state machine)

### 10. Permissions
- Management users: Can create, view, update orders
- Admin users: Can also delete orders and customers

## User Experience Flows

### Creating a Purchase Order:
1. Click "Create Order" from orders page
2. Select customer from dropdown (or create new inline)
3. Add product line items:
   - Select product type
   - Enter quantity
   - Click "Add Item"
   - Repeat for more items
4. Review items table
5. Click "Create Order"
6. Redirected to order detail page

### Recording a Delivery:
1. View order detail page
2. Click "Add Delivery Update"
3. Enter note (e.g., "Delivered 50 food packs to customer")
4. Select product type delivered (optional)
5. Enter quantity delivered
6. Submit
7. Progress bar updates automatically
8. Update appears in history log

### Viewing Order Status:
1. Orders list page shows all orders
2. Filter by "In Progress" to see active orders
3. Click on order to see details
4. View progress bars for each item
5. See update history at bottom

## Database Optimization
- Add indexes:
  - `PurchaseOrder.status`
  - `PurchaseOrder.customer_id`
  - `PurchaseOrder.created_at`
- Use `select_related()` for customer queries
- Use `prefetch_related()` for items and updates

## Future Enhancements (Not in Initial Build)
- PDF invoice generation
- Email notifications to customers
- Inventory reservation system
- Automated status transitions
- Delivery scheduling calendar
- Customer portal (for customers to track their orders)

## File Structure After Implementation
```
kitchen-management-system/
├── core/
│   ├── templates/
│   │   └── core/
│   │       ├── customers/
│   │       └── orders/
│   ├── forms.py                 # All form classes
│   ├── views.py                 # All view functions/classes
│   └── urls.py                  # URL routing
```

## Testing Checklist
- [ ] Can create new customer
- [ ] Can create purchase order with multiple items
- [ ] Order detail shows correct information
- [ ] Can add delivery update
- [ ] Fulfillment quantities update correctly
- [ ] Progress bars display accurately
- [ ] Status changes automatically based on fulfillment
- [ ] Update history displays chronologically
- [ ] Can filter orders by status
- [ ] Can search for customers
- [ ] Cannot exceed quantity ordered when fulfilling
- [ ] Completed orders display differently

## Dependencies
```
# None required beyond base Django and Tailwind CSS
# Optional: django-filter for advanced filtering
# Optional: django-tables2 for table rendering
```

## Notes
- Keep order detail page clean and scannable
- Update history is critical - make it prominent
- Mobile-friendly for on-the-go order checking
- Fast order creation is important
- Consider printable order sheets for kitchen staff
