def pode_ver(usuario, alvo):
    if usuario.perfil == 'candidato':
        return True
    return alvo.superior == usuario
