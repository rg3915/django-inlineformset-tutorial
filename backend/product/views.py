from django.shortcuts import render
from django.views.generic import ListView

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product


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
