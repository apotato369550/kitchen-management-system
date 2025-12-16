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
]
