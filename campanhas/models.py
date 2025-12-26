from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Candidato(models.Model):
    nome_urna = models.CharField(max_length=100, verbose_name="Nome de Urna")
    numero = models.CharField(max_length=10, verbose_name="Número")
    partido = models.CharField(max_length=20, verbose_name="Partido")
    cargo = models.CharField(max_length=100, verbose_name="Cargo", blank=True, null=True)
    meta_votos_total = models.PositiveIntegerField(default=0, verbose_name="Meta Geral de Votos")

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

    def __str__(self):
        return f"{self.nome_urna} ({self.numero})"

@receiver(post_save, sender=Candidato)
def criar_acesso_candidato(sender, instance, created, **kwargs):
    if created:
        from contas.models import Usuario
        username = instance.nome_urna.lower().replace(" ", "")
        if not Usuario.objects.filter(username=username).exists():
            Usuario.objects.create_user(
                username=username,
                password=f"votar{instance.numero}",
                is_staff=True,
                cargo="Candidato"
            )
