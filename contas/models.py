from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo/Função")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_custom_set',
        blank=True,
        verbose_name="Grupos"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_custom_permissions_set',
        blank=True,
        verbose_name="Permissões"
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
