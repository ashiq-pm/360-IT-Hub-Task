from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    service_name = models.CharField(max_length=255)
    payment_terms = models.TextField()
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_package = models.CharField(max_length=255)
    service_tax = models.DecimalField(max_digits=5, decimal_places=2)
    service_image = models.ImageField(upload_to='services/', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name
    
