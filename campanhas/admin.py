from django.contrib import admin
from .models import Candidato, Lideranca, Eleitor

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nome_urna', 'numero', 'partido')

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel', 'municipio_base')
    list_filter = ('nivel', 'municipio_base')

@admin.register(Eleitor)
class EleitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'zona', 'secao', 'cadastrado_por')
    search_fields = ('nome', 'titulo_eleitor', 'municipio')
