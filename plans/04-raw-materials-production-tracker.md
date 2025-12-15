# Raw Materials + Production Tracker Plan

## Goal
Build a daily tracking system for raw materials consumed and production output. Keep it simple and straightforward - no conversion relationships between inputs and outputs.

## Features Overview

### 1. Raw Materials Tracker
- Daily recording of consumed raw materials
- Categories: Meat, Vegetables, Oil, Miscellaneous (packaging)
- Flexible measurements: grams, pieces, heads, etc.
- View history by date and material

### 2. Production Tracker
- Daily recording of production output
- Product types: Food Packs, Platters/Bilao, custom types
- Quantity tracking
- Contents description for each output

## Implementation Steps

### 1. Admin Panel Setup
Register models in `core/admin.py`:
- RawMaterial
- DailyConsumption
- ProductType
- DailyProduction

Quick wins with Django admin before building custom UI.

### 2. Create Raw Materials Management UI

#### Views Needed:
1. **Raw Materials Library** (`/raw-materials/`)
   - List all raw materials with categories
   - Add new raw material (name, category, unit)
   - Edit/delete raw materials
   - Filter by category

2. **Daily Consumption Entry** (`/consumption/add/`)
   - Date picker (default: today)
   - Select raw material from dropdown
   - Enter quantity
   - Quick add multiple entries for same day
   - Submit form

3. **Consumption History** (`/consumption/`)
   - Table view grouped by date (most recent first)
   - Columns: Date, Material, Quantity, Category
   - Filter by: Date range, Category, Material
   - Export to CSV (optional, future feature)

### 3. Create Production Management UI

#### Views Needed:
1. **Product Types Library** (`/product-types/`)
   - List all product types
   - Add new product type (name, description)
   - Edit/delete product types

2. **Daily Production Entry** (`/production/add/`)
   - Date picker (default: today)
   - Select product type from dropdown
   - Enter quantity produced
   - Optional: Contents description (text field)
   - Quick add multiple entries for same day
   - Submit form

3. **Production History** (`/production/`)
   - Table view grouped by date (most recent first)
   - Columns: Date, Product Type, Quantity, Contents
   - Filter by: Date range, Product Type
   - Export to CSV (optional, future feature)

### 4. Dashboard View (Optional but Recommended)
`/dashboard/` or `/` (homepage after login):
- Today's summary:
  - Number of raw materials consumed today
  - Total production output today
- Quick links to add consumption/production
- Recent activity (last 7 days)

### 5. UI/UX Design (Tailwind CSS)

#### Design Principles:
- Clean, minimalist interface
- Large, touch-friendly buttons (mobile usage in kitchen)
- Clear typography
- Consistent color scheme:
  - Primary: Blue (actions)
  - Success: Green (confirmations)
  - Warning: Yellow (alerts)
  - Danger: Red (delete actions)

#### Key Components:
- Data tables with Tailwind table classes
- Forms with clear labels and validation
- Date pickers (use HTML5 `<input type="date">` for simplicity)
- Dropdown selects with search (use `django-autocomplete-light` if needed)
- Responsive layout (mobile-first)

### 6. Forms Implementation

#### Raw Material Form:
```python
# forms.py
class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ['name', 'category', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.TextInput(attrs={'class': 'form-input'}),
        }
```

#### Daily Consumption Form:
```python
class DailyConsumptionForm(forms.ModelForm):
    class Meta:
        model = DailyConsumption
        fields = ['date', 'raw_material', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'raw_material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }
```

Similar forms for ProductType and DailyProduction.

### 7. URL Structure
```python
# core/urls.py
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Raw Materials
    path('raw-materials/', views.raw_material_list, name='raw_material_list'),
    path('raw-materials/add/', views.raw_material_create, name='raw_material_create'),
    path('raw-materials/<uuid:pk>/edit/', views.raw_material_edit, name='raw_material_edit'),
    path('raw-materials/<uuid:pk>/delete/', views.raw_material_delete, name='raw_material_delete'),

    # Consumption
    path('consumption/', views.consumption_history, name='consumption_history'),
    path('consumption/add/', views.consumption_create, name='consumption_create'),
    path('consumption/<uuid:pk>/delete/', views.consumption_delete, name='consumption_delete'),

    # Product Types
    path('product-types/', views.product_type_list, name='product_type_list'),
    path('product-types/add/', views.product_type_create, name='product_type_create'),
    path('product-types/<uuid:pk>/edit/', views.product_type_edit, name='product_type_edit'),
    path('product-types/<uuid:pk>/delete/', views.product_type_delete, name='product_type_delete'),

    # Production
    path('production/', views.production_history, name='production_history'),
    path('production/add/', views.production_create, name='production_create'),
    path('production/<uuid:pk>/delete/', views.production_delete, name='production_delete'),
]
```

### 8. Template Structure
```
core/templates/core/
├── base.html                      # Base template with Tailwind CDN
├── dashboard.html                 # Homepage/dashboard
├── raw_materials/
│   ├── list.html                  # Raw materials library
│   └── form.html                  # Add/edit raw material
├── consumption/
│   ├── list.html                  # Consumption history
│   └── form.html                  # Add consumption entry
├── product_types/
│   ├── list.html                  # Product types library
│   └── form.html                  # Add/edit product type
└── production/
    ├── list.html                  # Production history
    └── form.html                  # Add production entry
```

## Validation Rules
- Date cannot be in the future
- Quantity must be positive
- Raw material name must be unique
- Product type name must be unique

## User Experience Flow

### Adding Daily Consumption:
1. User clicks "Add Consumption" from dashboard
2. Form shows today's date (editable)
3. User selects material from dropdown
4. User enters quantity
5. User clicks "Save" or "Save & Add Another"
6. Success message appears
7. Redirected to consumption history or form (if adding another)

### Viewing History:
1. User clicks "Consumption History" from navigation
2. Table shows all entries, grouped by date
3. User can filter by date range or category
4. User can click on entry to view details or delete

## Performance Considerations
- Add database indexes on `date` fields for faster queries
- Paginate history views (50 entries per page)
- Use `select_related()` for foreign key queries to reduce DB hits

## Future Enhancements (Not in Initial Build)
- Bulk entry form (add multiple materials at once)
- Data visualization (charts/graphs)
- Export functionality
- Print-friendly views
- Mobile app (PWA)

## File Structure After Implementation
```
kitchen-management-system/
├── core/
│   ├── templates/
│   │   └── core/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── raw_materials/
│   │       ├── consumption/
│   │       ├── product_types/
│   │       └── production/
│   ├── static/
│   │   └── core/
│   │       ├── css/
│   │       │   └── styles.css  # Custom Tailwind overrides if needed
│   │       └── js/
│   │           └── forms.js     # Form enhancements (optional)
│   ├── forms.py                 # All form classes
│   ├── views.py                 # All view functions/classes
│   └── urls.py                  # URL routing
```

## Testing Checklist
- [ ] Can add new raw material
- [ ] Can record daily consumption
- [ ] Consumption history displays correctly
- [ ] Can filter consumption by date/category
- [ ] Can add new product type
- [ ] Can record daily production
- [ ] Production history displays correctly
- [ ] Date validation works (no future dates)
- [ ] Quantity validation works (positive numbers only)
- [ ] Forms display validation errors
- [ ] Dashboard shows today's activity

## Dependencies to Add
```
# None required beyond base Django and Tailwind CSS
# Optional: django-crispy-forms for better form rendering
# Optional: django-autocomplete-light for searchable dropdowns
```

## Notes
- Keep it simple - don't overcomplicate the UI
- Mobile-friendly is important (kitchen environment)
- Fast data entry is priority #1
- No conversion logic between raw materials and production (as requested)
