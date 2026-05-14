from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shopper.views import CreateOrderView, OrderSuccessView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('index/', include('index.urls')),
    path('commodity/', include('commodity.urls')),
    path('shopper/', include('shopper.urls')),
    path('cart/', include('shopper.urls')),
    path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
