from django.contrib import admin
from .models import Projecao

@admin.register(Projecao)
class ProjecaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'eleitor', 'percentual')
