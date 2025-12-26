from django.contrib import admin
from .models import Lideranca, AtendimentoSocial

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'nivel', 'meta_votos', 'telefone')
    list_filter = ('nivel', 'municipio')
    search_fields = ('nome', 'telefone')
    list_editable = ('meta_votos', 'nivel')
    list_per_page = 25

@admin.register(AtendimentoSocial)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('lideranca', 'status')
    list_filter = ('status',)
    search_fields = ('lideranca__nome', 'pedido')
