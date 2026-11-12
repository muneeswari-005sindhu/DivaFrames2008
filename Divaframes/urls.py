"""
URL configuration for Divaframes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from divapictures.views import FrameViewSet, home, create_payment, payment_success, order_page, my_orders
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'frames', FrameViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('order/<int:frame_id>/',order_page,name='order_page'),
    path('orders/', my_orders, name='my_orders'),
    path('api/', include(router.urls)),
    path('pay/<int:id>/', create_payment, name='pay'),
    path('payment/success/', payment_success, name='payment_success'),
]

# Images 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


