from django.urls import path

from backend.ecommerce import views as v

app_name = 'ecommerce'


urlpatterns = [
    path('', v.OrderListView.as_view(), name='order_list'),
    path('create/', v.order_create, name='order_create'),
    path('add-row/', v.add_row_order_items_hx, name='add_row_order_items_hx'),
    path('product/price/', v.product_price, name='product_price'),
    path('<int:pk>/update/', v.order_update, name='order_update'),
    path('order-item/<int:pk>/delete/', v.order_item_delete, name='order_item_delete'),
]
