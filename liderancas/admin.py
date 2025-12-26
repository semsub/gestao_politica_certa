from django.contrib import admin
from django.utils.html import format_html
from .models import Lideranca, AtendimentoSocial

@admin.register(Lideranca)
class LiderancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio', 'meta_votos', 'status_badge')
    list_filter = ('municipio', 'nivel')
    list_editable = ('meta_votos',)
    search_fields = ('nome',)

    def status_badge(self, obj):
        cores = {'A': '#28a745', 'B': '#ffc107', 'C': '#17a2b8'}
        return format_html(
            '<span style="background:{}; color:white; padding:5px 10px; border-radius:15px; font-weight:bold;">{}</span>',
            cores.get(obj.nivel, '#6c757d'),
            obj.get_nivel_display()
        )
    status_badge.short_description = "Influência"

@admin.register(AtendimentoSocial)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('lideranca', 'demanda', 'situacao')
    
    def situacao(self, obj):
        if obj.concluido:
            return format_html('<span style="color:green;">✔ RESOLVIDO</span>')
        return format_html('<span style="color:red;">⏳ PENDENTE</span>')
