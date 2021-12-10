from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    path('accounts/', include('backend.accounts.urls')),  # without namespace
    # path('ecommerce/', include('backend.ecommerce.urls', namespace='ecommerce')),
    path('product/', include('backend.product.urls', namespace='product')),
    path('admin/', admin.site.urls),
]
