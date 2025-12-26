from django.contrib import admin
from .models import Lideranca, AtendimentoSocial

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'meta_votos', 'nivel')
    list_editable = ('meta_votos', 'nivel')
    search_fields = ('nome', 'municipio__nome')
    list_per_page = 20
