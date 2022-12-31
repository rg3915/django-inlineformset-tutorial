from django.contrib import admin

from .models import Order, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsInline,)
    list_display = ('__str__', 'nf', 'provider')
    search_fields = ('nf',)
