from django.urls import path
from.import views
urlpatterns=[
    path('',views.home,name='home')
]

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'frames', views.FrameViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('order/<int:id>/', views.order_frame, name='order'),
    path('api/', include(router.urls)),

    path("payment/", views.payment_page, name="payment"),
    path("create-order/", views.create_order, name="create_order"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from divapictures.views import FrameViewSet, home
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'frames', FrameViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
