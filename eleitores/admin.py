from django.contrib import admin
from .models import Eleitor

@admin.register(Eleitor)
class EleitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'municipio', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'cpf')
