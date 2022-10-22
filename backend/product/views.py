from django.shortcuts import render
from django.views.generic import ListView

import django_tables2 as tables
from django.utils.html import format_html

from .forms import ProductForm
from .models import Product

class TotalColumn(tables.Column):
    def render(self, value):
        return format_html(f"""
                <a class="mr-10  btn-light mx-1px text-95" href="{value}" data-title="Details">
                    <i class="mr-1 fa fa-eye text-secondary-m1 text-120 w-2"></i>
                    Details
                </a>
                <a class="mr-10  btn-light mx-1px text-95" href="{value}/print" data-title="Print">
                    <i class="mr-1 fa fa-print text-primary-m1 text-120 w-2"></i>
                    Print
                </a>
                <a class="mr-10  btn-light mx-1px text-95" href="{value}/pdf" data-title="PDF">
                    <i class="mr-1 fa fa-file-pdf-o text-danger-m1 text-120 w-2"></i>
                    Export
                </a>
        """)

class ProductTable(tables.Table):
    title = tables.Column(linkify=True)
    details = TotalColumn(verbose_name = "See details / Print / Export", accessor="title", orderable=False, )

    class Meta:
        model = Product
        fields = ("title", "price" )
        per_page = 15
        attrs = {"class": "table table-striped table-hover"}


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
