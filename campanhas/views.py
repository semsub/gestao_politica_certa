from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Count
from .models import Candidato, Lideranca, Eleitor

# 1. CLASSE QUE ESTAVA FALTANDO (Registro de Apoio)
class RegistroVisitaView(APIView):
    def post(self, request):
        dados = request.data
        try:
            # Pegamos a primeira liderança como padrão se não for enviada
            lider_id = dados.get('lider_id')
            if not lider_id:
                lider = Lideranca.objects.first()
                lider_id = lider.id if lider else None

            Eleitor.objects.create(
                nome=dados.get('nome'),
                titulo_eleitor=dados.get('titulo'),
                zona=dados.get('zona', '0'),
                secao=dados.get('secao', '0'),
                tags=dados.get('tags', 'Apoio'),
                cadastrado_por_id=lider_id,
                latitude=dados.get('lat'),
                longitude=dados.get('lng'),
                municipio=dados.get('municipio', 'Salinópolis')
            )
            return Response({"status": "Sucesso"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 2. RANKING DE MILITÂNCIA
@api_view(['GET'])
def ranking_militancia(request):
    ranking = Lideranca.objects.annotate(total=Count('eleitor')).order_by('-total')
    dados = [{"nome": r.nome, "total": r.total} for r in ranking]
    return Response(dados)

# 3. RELATÓRIO TERRITORIAL
@api_view(['GET'])
def relatorio_territorial(request):
    relatorio = Eleitor.objects.values('municipio').annotate(votos=Count('id')).order_by('-votos')
    return Response(list(relatorio))

# 4. MAPA DE CALOR
@api_view(['GET'])
def mapa_calor_votos(request):
    pontos = Eleitor.objects.exclude(latitude__isnull=True).values('latitude', 'longitude', 'nome')
    return Response(list(pontos))
