from django.urls import path

from backend.product import views as v

app_name = 'product'


urlpatterns = [
    path('', v.ProductListView.as_view(), name='product_list'),
    path('create/', v.product_create, name='product_create'),
]
