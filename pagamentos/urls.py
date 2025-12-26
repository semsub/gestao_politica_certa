from django.urls import path
from .views import pagar

urlpatterns = [
    path('pix/<int:campanha_id>/<int:valor>/', pagar),
]
