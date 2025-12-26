from django.contrib import admin
from .models import Lideranca, AtendimentoSocial, RegiaoIntegracao, CategoriaAcao

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'municipio', 'regiao', 'created_at') # created_at agora existe

@admin.register(AtendimentoSocial)
class AtendimentoAdmin(admin.ModelAdmin):
    # list_display[4] era o created_at que estava dando erro. Agora está resolvido.
    list_display = ('eleitor_nome', 'lideranca', 'categoria', 'status', 'created_at')
