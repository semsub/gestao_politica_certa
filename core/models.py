from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True, verbose_name="Registro Ativo")

    class Meta:
        abstract = True

# --- App: Campanhas ---
class Campanha(BaseModel):
    nome = models.CharField(max_length=200, verbose_name="Nome da Campanha")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição/Objetivo")
    meta_votos = models.PositiveIntegerField(default=0)
    orcamento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

# --- App: Lideranças ---
class Lideranca(BaseModel):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='liderancas')
    municipio = models.ForeignKey('municipios.Municipio', on_delete=models.SET_NULL, null=True)
    votos_estimados = models.IntegerField(default=0)
    meta_individual = models.IntegerField(default=100)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Liderança"
        ordering = ['-votos_estimados']

    def __str__(self):
        return f"{self.usuario.nome} ({self.municipio})"
