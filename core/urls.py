from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
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
    path('orders/<uuid:pk>/update/', views.purchase_order_add_update, name='purchase_order_add_update'),
    path('orders/<uuid:pk>/status/', views.purchase_order_change_status, name='purchase_order_change_status'),
    path('orders/<uuid:pk>/delete/', views.purchase_order_delete, name='purchase_order_delete'),
]
