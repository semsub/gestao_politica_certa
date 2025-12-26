from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .models import AtendimentoSocial, Lideranca
from .serializers import CustomTokenSerializer, AtendimentoSerializer

class LoginLiderancaView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class SincronizarVotosView(generics.CreateAPIView):
    serializer_class = AtendimentoSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        lideranca = Lideranca.objects.get(usuario=self.request.user)
        serializer.save(lideranca=lideranca)

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        lideranca = Lideranca.objects.filter(usuario=request.user).first()
        votos = AtendimentoSocial.objects.filter(lideranca=lideranca).count()
        return Response({
            "votos_contabilizados": votos,
            "meta": lideranca.meta_eleitores if lideranca else 0,
            "progresso": (votos / lideranca.meta_eleitores * 100) if lideranca and lideranca.meta_eleitores > 0 else 0
        })

class MapaCalorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pontos = AtendimentoSocial.objects.exclude(latitude__isnull=True).values(
            'eleitor_nome', 'latitude', 'longitude', 'categoria__nome'
        )
        return Response(list(pontos))
