from django.db import models

class Lideranca(models.Model):
    # Quem cadastrou este líder? (Rastreabilidade total)
    cadastrado_por = models.ForeignKey('campanhas.Coordenador', on_delete=models.SET_NULL, null=True)
    
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    whatsapp = models.CharField(max_length=20)
    municipio = models.CharField(max_length=100) # Ex: 144 cidades do Pará
    
    # Lógica de exclusividade solicitada:
    apoiando_outros = models.BooleanField(
        default=False, 
        help_text="Se Falso, trabalha apenas para este Candidato Majoritário"
    )
    
    # Status de acesso (Só entra no app após o Coordenador ativar)
    acesso_liberado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.municipio}"
