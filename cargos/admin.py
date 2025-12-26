from django.contrib import admin
from .models import Cargo

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'eletivo', 'permite_reeleicao')
    list_filter = ('eletivo',)
    search_fields = ('nome',)
