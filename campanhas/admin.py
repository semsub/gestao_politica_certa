from django.contrib import admin
from .models import Campanha

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'criado_em', 'atualizado_em')
    readonly_fields = ('criado_em', 'atualizado_em')
