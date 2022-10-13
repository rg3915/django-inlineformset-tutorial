from django.shortcuts import render
from django.views.generic import ListView

import django_tables2 as tables

from .forms import ProductForm
from .models import Product


class ProductTable(tables.Table):
    title = tables.Column(linkify=True)  

    class Meta:
        model = Product
        fields = ("title", "price")
        per_page = 10


class ProductListView(tables.SingleTableView):
    model = Product
    table_class = ProductTable


def product_create(request):
    template_name = 'hx/product_form_hx.html'
    form = ProductForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
            template_name = 'hx/product_result_hx.html'
            context = {'object': product}
            return render(request, template_name, context)

    context = {'form': form}
    return render(request, template_name, context)
