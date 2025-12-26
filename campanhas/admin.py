from django.contrib import admin
from .models import Candidato

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    # Removido 'ativo' para evitar erros de sistema
    list_display = ('nome_urna', 'numero', 'partido', 'cargo', 'meta_votos_total')
    search_fields = ('nome_urna', 'numero')
    list_filter = ('partido', 'cargo')
