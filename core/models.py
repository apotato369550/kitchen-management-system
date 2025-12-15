import uuid
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'


class RawMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('meat', 'Meat'),
        ('vegetables', 'Vegetables'),
        ('oil', 'Oil'),
        ('miscellaneous', 'Miscellaneous'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=50)  # e.g., grams, pieces, heads

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        db_table = 'raw_materials'


class DailyConsumption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='consumptions')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.raw_material.name} - {self.date}"

    class Meta:
        db_table = 'daily_consumptions'
        ordering = ['-date', '-created_at']


class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # e.g., "Food Pack", "Platter", "Bilao"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_types'


class DailyProduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='productions')
    quantity = models.IntegerField()
    contents_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_type.name} - {self.date}"

    class Meta:
        db_table = 'daily_productions'
        ordering = ['-date', '-created_at']


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO-{str(self.id)[:8]} - {self.customer.name}"

    class Meta:
        db_table = 'purchase_orders'
        ordering = ['-created_at']


class PurchaseOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    quantity_fulfilled = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_type.name} x{self.quantity_ordered}"

    class Meta:
        db_table = 'purchase_order_items'


class PurchaseOrderUpdate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='updates')
    note = models.TextField()  # comment-style update
    quantity_delivered = models.IntegerField(blank=True, null=True)  # for staggered fulfillment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.purchase_order}"

    class Meta:
        db_table = 'purchase_order_updates'
        ordering = ['-created_at']
