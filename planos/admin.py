from django.contrib import admin
from .models import Plano

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'valor')
    search_fields = ('nome',)
