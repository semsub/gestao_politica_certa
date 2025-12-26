from planos.models import Plano

Planos = [
    {
        "nome": "Básico",
        "preco": 199,
        "max_liderancas": 20,
        "max_municipios": 5,
        "mapa_eleitoral": False,
        "projecao_votos": False,
        "dashboard": True
    },
    {
        "nome": "Profissional",
        "preco": 499,
        "max_liderancas": 100,
        "max_municipios": 30,
        "mapa_eleitoral": True,
        "projecao_votos": True,
        "dashboard": True
    },
    {
        "nome": "Premium",
        "preco": 999,
        "max_liderancas": 1000,
        "max_municipios": 144,
        "mapa_eleitoral": True,
        "projecao_votos": True,
        "dashboard": True
    }
]

for p in Planos:
    Plano.objects.get_or_create(**p)

print("✔ Planos criados com sucesso")
