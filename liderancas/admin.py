from django.contrib import admin
from django.utils.html import format_html
from .models import Lideranca, AtendimentoSocial

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'meta_votos', 'exibir_nivel')
    list_filter = ('municipio', 'nivel')
    search_fields = ('nome',)
    list_editable = ('meta_votos',)

    def exibir_nivel(self, obj):
        cores = {'A': 'green', 'B': 'orange', 'C': 'blue'}
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            cores.get(obj.nivel, 'gray'),
            obj.get_nivel_display()
        )
    exibir_nivel.short_description = "Status"

@admin.register(AtendimentoSocial)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('lideranca', 'demanda', 'status_visual')
    
    def status_visual(self, obj):
        if obj.concluido:
            return format_html('<b style="color: green;">✔ CONCLUÍDO</b>')
        return format_html('<b style="color: red;">⏳ PENDENTE</b>')
