from .usuario import buscar_por_email

def autenticar(email, contraseña):
    usuario = buscar_por_email(email)

    if usuario is None:
        return None

    if usuario["contraseña"] != contraseña:
        return None

    return usuario
