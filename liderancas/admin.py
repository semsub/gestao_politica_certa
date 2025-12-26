from django.contrib import admin
from .models import Lideranca, AtendimentoSocial

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'meta_votos', 'nivel')
    list_filter = ('municipio', 'nivel')
    search_fields = ('nome', 'telefone')
    list_editable = ('meta_votos', 'nivel')

@admin.register(AtendimentoSocial)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('lideranca', 'concluido', 'data_registro')
    list_filter = ('concluido',)
