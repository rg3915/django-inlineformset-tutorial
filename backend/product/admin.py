from django.contrib import admin

from .models import Product, Provider


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'manufacturing_date', 'due_date', 'provider')
    search_fields = ('title',)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
