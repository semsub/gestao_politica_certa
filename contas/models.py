from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
