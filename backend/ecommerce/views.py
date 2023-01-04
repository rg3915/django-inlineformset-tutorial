import json
import logging

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView

from backend.product.models import Product, Provider

from .forms import OrderForm, OrderItemsForm, OrderItemsFormset
from .models import Order, OrderItems


class OrderListView(ListView):
    model = Order


def order_create(request):
    template_name = 'ecommerce/order_form.html'
    order_instance = Order()

    form = OrderForm(request.POST or None, instance=order_instance, prefix='main')
    formset = OrderItemsFormset(request.POST or None, instance=order_instance, prefix='items')

    lista = [f.fields for f in formset][0]  # dict_keys
    *formset_fields, = lista  # transforma dict_keys em lista

    if 'id' in formset_fields:
        formset_fields.remove('id')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('ecommerce:order_list')

    providers = Provider.objects.all()
    context = {
        'form': form,
        'formset': formset,
        'providers': providers,
        'formset_fields': json.dumps(formset_fields)
    }
    return render(request, template_name, context)


def add_row_order_items_hx(request):
    template_name = 'ecommerce/hx/row_order_items_hx.html'
    form = OrderItemsForm()

    products = Product.objects.all()
    try:
        provider = request.GET['main-provider']
        provider = int(provider)
        if provider:
            products = products.filter(provider__id=provider)
    except ValueError:
        logging.info('Valor inválido para main-provider')

    context = {'order_item_form': form, 'products': products}
    return render(request, template_name, context)


def products_by_provider(request):
    template_name = 'ecommerce/hx/products_select_hx.html'
    url = request.get_full_path()
    item = url.split('-')[1]
    provider_pk = list(request.GET.values())[0]
    products = Product.objects.filter(provider__id=provider_pk)

    context = {'products': products, 'item': item[0]}
    return render(request, template_name, context)


def product_price(request):
    template_name = 'ecommerce/hx/product_price_hx.html'
    url = request.get_full_path()
    item = url.split('-')[1]
    product_pk = list(request.GET.values())[0]
    product = Product.objects.get(pk=product_pk)

    context = {'product': product, 'item': item[0]}
    return render(request, template_name, context)


def order_update(request, pk):
    template_name = 'ecommerce/order_form.html'
    order_instance = Order.objects.get(pk=pk)

    form = OrderForm(request.POST or None, instance=order_instance, prefix='main')
    formset = OrderItemsFormset(request.POST or None, instance=order_instance, prefix='items')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('ecommerce:order_list')

    providers = Provider.objects.all()
    context = {'form': form, 'formset': formset, 'providers': providers}
    return render(request, template_name, context)


def order_item_delete(request, pk):
    order_item = OrderItems.objects.get(pk=pk)
    order_item.delete()
    return HttpResponse('')
