from django.contrib import admin
from .models import Regiao

@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
