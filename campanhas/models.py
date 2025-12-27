from django.db import models
from django.contrib.auth.models import User

class Candidato(models.Model):
    usuario_root = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_urna = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    partido = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50, default="Vereador")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_urna} ({self.numero})"

class Lideranca(models.Model):
    NIVEL = [('COORDENADOR', 'Coordenador'), ('LIDER', 'Líder de Bairro'), ('VOLUNTARIO', 'Voluntário')]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20, choices=NIVEL, default='VOLUNTARIO')
    indicado_por = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    municipio_base = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.nivel}"

class Eleitor(models.Model):
    nome = models.CharField(max_length=200)
    titulo_eleitor = models.CharField(max_length=20, unique=True)
    zona = models.CharField(max_length=10)
    secao = models.CharField(max_length=10)
    tags = models.CharField(max_length=255, help_text="Ex: Saúde, Igreja, Universitário")
    cadastrado_por = models.ForeignKey(Lideranca, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    municipio = models.CharField(max_length=100, default="Salinópolis")
    votos_no_domicilio = models.IntegerField(default=1)
    data_visita = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class BoletimUrna(models.Model):
    municipio = models.CharField(max_length=100)
    zona = models.CharField(max_length=10)
    secao = models.CharField(max_length=10)
    votos_nosso_candidato = models.IntegerField()
    foto_comprovante = models.ImageField(upload_to='bus/', null=True, blank=True)
    fiscal_responsavel = models.ForeignKey(Lideranca, on_delete=models.CASCADE)

    def __str__(self):
        return f"BU: {self.municipio} - Seção {self.secao}"
