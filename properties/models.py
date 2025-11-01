from django.db import models
from uuid import uuid4

class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, null=False)
    created_at = models.DateField(auto_now_add=True)
    
