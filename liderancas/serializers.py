from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import AtendimentoSocial

class CustomTokenSerializer(TokenObtainPairSerializer):
    # Define explicitamente que o campo de login é o e-mail
    def validate(self, attrs):
        # Mapeia o campo 'email' vindo do App para o 'username' que o Django espera internamente
        email = attrs.get("email")
        password = attrs.get("password")
        
        attrs['username'] = email
        return super().validate(attrs)

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtendimentoSocial
        fields = ['eleitor_nome', 'categoria', 'descricao', 'latitude', 'longitude', 'status']
