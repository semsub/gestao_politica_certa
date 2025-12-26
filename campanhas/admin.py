from django.contrib import admin
from .models import Candidato

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nome_urna', 'numero', 'partido', 'ativo')
    list_filter = ('ativo',)
