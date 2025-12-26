def contar_votos(usuario):
    votos = 0
    for sub in usuario.subordinados.all():
        votos += 1
        votos += contar_votos(sub)
    return votos
