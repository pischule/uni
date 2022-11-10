from django.contrib import admin

from .models import Product, Order, ProductInstance


admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductInstance)
