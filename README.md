# django-inlineformset-tutorial

Django inlineformset_factory + HTMX

## Este projeto foi feito com:

* [Python 3.9.8](https://www.python.org/)
* [Django 3.2.10](https://www.djangoproject.com/)
* [Bootstrap 4.0](https://getbootstrap.com/)
* [htmx 1.6.1](https://htmx.org/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-inlineformset-tutorial.git
cd django-inlineformset-tutorial
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

## Passo a passo

**Objetivo:** Nosso objetivo será inserir vários produtos numa ordem de compra. E veja o Admin.

> Considere a app `product` e `ecommerce`.

## Produtos

Os produtos são adicionados via modal com HTMX.

* Mostrar o htmx importado em `base.html`.

* Mostrar

```html
<!-- product_list.html -->
<a
  href=""
  class="btn btn-primary"
  data-toggle="modal"
  data-target="#addModal"
  hx-get="{% url 'product:product_create' %}"
  hx-target="#addContent"
  hx-swap="innerHTML"
>Adicionar</a>
```

```python
# product/views.py
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
```

## Ordem de compra

* Mostrar o `models.py`.

* Mostrar o `admin.py`

```python
# ecommerce/admin.py
class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsInline,)
    list_display = ('__str__', 'nf',)
    search_fields = ('nf',)
```

> Rodar o Admin.

Editar `forms.py`

```python
# ecommerce/forms.py
from django import forms
from django.forms import inlineformset_factory

from .models import Order, OrderItems


class OrderForm(forms.ModelForm):
    required_css_class = 'required'

    nf = forms.IntegerField(label="Nota Fiscal")

    class Meta:
        model = Order
        fields = ('nf',)


class OrderItemsForm(forms.ModelForm):
    required_css_class = 'required'

    id = forms.IntegerField()

    class Meta:
        model = OrderItems
        fields = ('order', 'id', 'product', 'quantity', 'price')

    def __init__(self, *args, **kwargs):
        super(OrderItemsForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['order'].label = ''
        self.fields['order'].widget = forms.HiddenInput()

        self.fields['id'].label = ''
        self.fields['id'].widget = forms.HiddenInput()


OrderItemsFormset = inlineformset_factory(
    Order,
    OrderItems,
    form=OrderItemsForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
)
```

Editar `views.py`

```python
# ecommerce/views.py
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView

from backend.product.models import Product

from .forms import OrderForm, OrderItemsForm, OrderItemsFormset
from .models import Order, OrderItems


class OrderListView(ListView):
    model = Order


def order_create(request):
    template_name = 'ecommerce/order_form.html'
    order_instance = Order()

    form = OrderForm(request.POST or None, instance=order_instance, prefix='main')
    formset = OrderItemsFormset(request.POST or None, instance=order_instance, prefix='items')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('ecommerce:order_list')

    context = {'form': form, 'formset': formset}
    return render(request, template_name, context)

```

Editar `urls.py`

```python
# ecommerce/urls.py
from django.urls import path

from backend.ecommerce import views as v

app_name = 'ecommerce'


urlpatterns = [
    path('', v.OrderListView.as_view(), name='order_list'),
    path('create/', v.order_create, name='order_create'),
    # path('add-row/', v.add_row_order_items_hx, name='add_row_order_items_hx'),
    # path('product/price/', v.product_price, name='product_price'),
    # path('<int:pk>/update/', v.order_update, name='order_update'),
    # path('order-item/<int:pk>/delete/', v.order_item_delete, name='order_item_delete'),
]
```

Criar pastas e templates

```
mkdir -p backend/ecommerce/templates/ecommerce/hx
touch backend/ecommerce/templates/ecommerce/order_{list,form}.html
touch backend/ecommerce/templates/ecommerce/hx/{product_price,row_order_items}_hx.html
tree
```

* Mostrar a `order_list.html` já pronta.

Editar `order_form.html`

```html
<!-- order_list.html -->
{% extends "base.html" %}
{% load static %}
{% load widget_tweaks %}

{% block css %}

  <style>
    .form-control {
      margin: 10px;
    }
    .legend {
      border-bottom: 1px solid #e5e5e5;
    }
  </style>

{% endblock css %}

{% block content %}

<div class="row">
  <div class="cols">
    <form method="POST" novalidate>
      {% csrf_token %}

      <legend class="legend">Ordem de compra</legend>

      <div class="row">
        <div class="col-sm-6">
          {% for field in form.visible_fields %}
            <div class="form-group">
              <label for="{{ field.id_for_label }}">
                {% if field.field.required %}
                  <span class="required">{{ field.label }} </span>
                {% else %}
                  {{ field.label }}
                {% endif %}
              </label>

              {% render_field field class="form-control" %}

              {% for error in field.errors %}
                <span class="text-muted">{{ error }}</span>
              {% endfor %}
            </div>
          {% endfor %}

        {{ formset.management_form }}

        </div>
      </div>

      <div class="row">
        <div class="col-sm-12">

          <legend class="legend">Itens</legend>

          <div id="order" class="form-inline">

            {% for order_item_form in formset %}
              <div id="item-{{ forloop.counter0 }}" class="form-group">
                {{ order_item_form.order }}
                {{ order_item_form.id }}

                {{ order_item_form.product.label }}
                {% render_field order_item_form.product class="form-control" hx-get="/ecommerce/product/price/" hx-target="#id_items-0-price" hx-swap="outerHTML" %}

                {{ order_item_form.quantity.label }}
                {{ order_item_form.quantity }}

                {{ order_item_form.price.label }}
                {{ order_item_form.price }}

                {% if order_item_form.id.value %}
                  <span
                    class="span-is-link no ml-2 remove-row"
                    hx-delete="{% url 'ecommerce:order_item_delete' order_item_form.id.value %}"
                    hx-target="#item-{{ forloop.counter0 }}"
                    hx-swap="outerHTML"
                  >
                    <i class="fa fa-times fa-lg"></i>
                  </span>
                {% else %}
                  <span class="span-is-link no ml-2" onclick="removeRow()">
                    <i class="fa fa-times fa-lg"></i>
                  </span>
                {% endif %}
              </div>
            {% endfor %}

          </div>

        </div>
      </div>

      <span
        id="addItem"
        class="btn btn-info mt-2"
        hx-get="{% url 'ecommerce:add_row_order_items_hx' %}"
        hx-target="#order"
        hx-swap="beforeend"
      >
        <i class="fa fa-plus"></i>
        Adicionar
      </span>

      <div class="row float-right">
        <div class="col-sm-12 mt-2">
          <div class="form-inline buttons">
            <button class="btn btn-primary" type="submit">
              <i class="fa fa-floppy-o"></i>
              Salvar
            </button>
            <a
              id="btn-close"
              href="{% url 'ecommerce:order_list' %}"
              class="btn btn-primary"
              style="display: none"
            >
              <i class="fa fa-close"></i>
              Fechar
            </a>
            <a
              href="{% url 'ecommerce:order_list' %}"
              class="btn btn-danger ml-2"
            >
              <i class="fa fa-times"></i>
              Cancelar
            </a>
          </div>
        </div>
      </div>

    </form>
  </div>
</div>

{% endblock content %}

{% block js %}

<script src="{% static 'js/main.js' %}"></script>

<script>
// Necessário por causa do delete
document.body.addEventListener('htmx:configRequest', (event) => {
  event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
</script>

{% endblock js %}

```

Editar `views.py`

```python
# ecommerce/views.py

def add_row_order_items_hx(request):
    template_name = 'ecommerce/hx/row_order_items_hx.html'
    form = OrderItemsForm()
    context = {'order_item_form': form}
    return render(request, template_name, context)

```

Editar `hx/row_order_items_hx.html`

```html
<!-- hx/row_order_items_hx.html -->
{% load widget_tweaks %}

<div id="item-{{ forloop.counter0 }}" class="form-group">

  <div class="form-group">
    {% render_field order_item_form.order data-field='order' %}

    <label>{{ order_item_form.product.label }}</label>
    {% render_field order_item_form.product class="form-control" hx-get="/ecommerce/product/price/" hx-target="#id_price" hx-swap="outerHTML" data-field='product' %}

    <label>{{ order_item_form.quantity.label }}</label>
    {% render_field order_item_form.quantity class="form-control" data-field='quantity' %}

    <label>{{ order_item_form.price.label }}</label>
    {% render_field order_item_form.price class="form-control" data-field='price' %}
  </div>

  <span class="span-is-link no ml-2" onclick="removeRow()">
    <i class="fa fa-times fa-lg"></i>
  </span>

</div>

```

* Mostrar `core/static/js/main.js`

> Mostrar a aplicação rodando.


## Retornando o preço do produto

Editar `views.py`

```python
# ecommerce/views.py

def product_price(request):
    template_name = 'ecommerce/hx/product_price_hx.html'
    url = request.get_full_path()
    print('url', url)
    print(url.split('-'))
    item = url.split('-')[1]
    print('item', item)
    print('list', list(request.GET.values()))
    product_pk = list(request.GET.values())[0]
    print('product_pk', product_pk)
    product = Product.objects.get(pk=product_pk)

    context = {'product': product, 'item': item[0]}
    return render(request, template_name, context)

```

Editar `hx/product_price_hx.html`

```html
<!-- hx/product_price_hx.html -->
<input
  id="id_items-{{item}}-price"
  name="items-{{item}}-price"
  class="form-control"
  type="number"
  data-field="price"
  value="{{ product.price|safe }}"
/>

```

## Editar

Edite `views.py`

```python
# ecommerce/views.py

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

    context = {'form': form, 'formset': formset}
    return render(request, template_name, context)
```

## Deletar

Edite `views.py`

```python
# ecommerce/views.py

def order_item_delete(request, pk):
    order_item = OrderItems.objects.get(pk=pk)
    order_item.delete()
    return HttpResponse('')

```

