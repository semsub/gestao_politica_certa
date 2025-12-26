from django.db import models

class Municipio(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='PA')
    # Adicionando a relação com a Região de Integração do app liderancas
    regiao = models.ForeignKey(
        'liderancas.RegiaoIntegracao', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='municipios_da_regiao'
    )

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.estado}"
