cat <<EOF > contas/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Usando related_name para evitar o erro E304 que você recebeu
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True
    )
    telefone = models.CharField(max_length=20, blank=True)
EOF
