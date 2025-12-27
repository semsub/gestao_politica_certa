from django.urls import path
from . import views

urlpatterns = [
    path('registro-visita/', views.RegistroVisitaView.as_view(), name='registro_visita'),
    path('ranking-militancia/', views.ranking_militancia, name='ranking_militancia'),
    path('relatorio-territorial/', views.relatorio_territorial, name='relatorio_territorial'),
    path('mapa-calor/', views.mapa_calor_votos, name='mapa_calor'),
]
