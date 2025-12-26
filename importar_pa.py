cat <<EOF > importar_pa.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from municipios.models import Municipio

cidades_pa = [
    "Abaetetuba", "Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", "Almeirim", "Altamira",
    "Anajás", "Ananindeua", "Anapu", "Augusto Corrêa", "Aurora do Pará", "Aveiro", "Bagre", "Baião",
    "Bannach", "Barcarena", "Belém", "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito",
    "Bragança", "Brasil Novo", "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru",
    "Cachoeira do Arari", "Cachoeira do Piriá", "Caetanoópolis", "Cametá", "Canaã dos Carajás",
    "Capanema", "Capitão Poço", "Castanhal", "Chaves", "Colares", "Conceição do Araguaia",
    "Concórdia do Pará", "Cumaru do Norte", "Curionópolis", "Curuá", "Curuçá", "Dom Eliseu",
    "Eldorado do Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", "Goianésia do Pará",
    "Gurupá", "Igarapé-Açu", "Igarapé-Miri", "Inhangapi", "Ipixuna do Pará", "Irituia", "Itaituba",
    "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Limoeiro do Ajuru", "Mãe do Rio", 
    "Magalhães Barata", "Marabá", "Maracanã", "Marapanim", "Marituba", "Medicilândia", "Melgaço",
    "Mocajuba", "Moju", "Mojuí dos Campos", "Monte Alegre", "Muaná", "Nova Esperança do Piriá",
    "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Novo Repartimento", "Óbidos", "Oeiras do Pará",
    "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Palestina do Pará", "Paragominas",
    "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", "Ponta de Pedras", "Portel",
    "Porto de Moz", "Prainha", "Primavera", "Quatipuru", "Redenção", "Rio Maria", "Rondon do Pará",
    "Rurópolis", "Salinópolis", "Salvaterra", "Santa Bárbara do Pará", "Santa Cruz do Arari",
    "Santa Izabel do Pará", "Santa Luzia do Pará", "Santa Maria das Barreiras", "Santa Maria do Pará",
    "Santana do Araguaia", "Santarém", "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas",
    "São Domingos do Araguaia", "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará",
    "São Geraldo do Araguaia", "São João da Ponta", "São João de Pirabas", "São João do Araguaia",
    "São Miguel do Guamá", "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio",
    "Soure", "Tailândia", "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão",
    "Tucumã", "Tucuruí", "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"
]

for cidade in cidades_pa:
    obj, created = Municipio.objects.get_or_create(nome=cidade, estado='PA')
    if created:
        print(f"✅ {cidade} adicionado.")
    else:
        print(f"🟡 {cidade} já existia.")

print("\n🚀 Base de dados do Pará atualizada com sucesso!")
EOF
