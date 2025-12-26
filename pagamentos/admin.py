from django.contrib import admin
from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'valor', 'data_pagamento')
    list_filter = ('data_pagamento',)
