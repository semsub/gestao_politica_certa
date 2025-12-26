from django.contrib import admin
from django.urls import path
from liderancas.views import (
    LoginLiderancaView, 
    SincronizarVotosView, 
    DashboardDataView, 
    MapaCalorView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginLiderancaView.as_view(), name='api_login'),
    path('api/v1/sincronizar/', SincronizarVotosView.as_view(), name='api_sync'),
    path('api/v1/dashboard/', DashboardDataView.as_view(), name='api_dash'),
    path('api/v1/mapa/', MapaCalorView.as_view(), name='api_mapa'),
]
