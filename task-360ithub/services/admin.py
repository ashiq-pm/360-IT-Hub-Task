from django.contrib import admin
from .models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_price', 'service_package', 'service_tax', 'user')
    search_fields = ('service_name', 'user__username')
    list_filter = ('service_price', 'service_tax')
    
admin.site.register(Service, ServiceAdmin)