from regioes.models import Regiao
from municipios.models import Municipio

dados = {
"Metropolitana":["Belém","Ananindeua","Marituba","Benevides","Santa Bárbara do Pará"],
"Rio Caeté":["Salinópolis","Bragança","Capanema","Primavera","Quatipuru","Tracuateua","Augusto Corrêa","Viseu","Peixe-Boi"],
"Guamá":["Castanhal","Inhangapi","Santa Isabel do Pará","São Miguel do Guamá"],
"Marajó":["Breves","Portel","Melgaço","Afuá","Chaves","Salvaterra","Soure"],
"Baixo Amazonas":["Santarém","Alenquer","Monte Alegre","Óbidos","Oriximiná","Juruti","Prainha","Terra Santa"],
"Carajás":["Marabá","Parauapebas","Canaã dos Carajás","Curionópolis","Eldorado dos Carajás","São Domingos do Araguaia"],
"Araguaia":["Redenção","Xinguara","Conceição do Araguaia","Santana do Araguaia"],
"Tocantins":["Cametá","Abaetetuba","Moju","Igarapé-Miri","Tailândia"],
"Xingu":["Altamira","Uruará","Placas","Medicilândia","Anapu"],
"Tapajós":["Itaituba","Jacareacanga","Novo Progresso","Trairão"],
"Rio Capim":["Paragominas","Ulianópolis","Dom Eliseu"],
"Lago de Tucuruí":["Tucuruí","Breu Branco","Goianésia do Pará"]
}

for r, ms in dados.items():
    regiao,_ = Regiao.objects.get_or_create(nome=r)
    for m in ms:
        Municipio.objects.get_or_create(nome=m, regiao=regiao)

print("✔ Pará carregado")
