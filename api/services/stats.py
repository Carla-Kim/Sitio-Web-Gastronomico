from ..database import stats

def obtener_stats():
    reservas = stats.obtener_reservas_por_mes()
    usuarios = stats.obtener_usuarios_por_rol()
    resenas = stats.obtener_promedios_de_resenas()
    menu = stats.obtener_productos_por_categoria()

    meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    results = {
        "reservas": {
            "meses": [meses[r["mes"]] for r in reservas],
            "cantidades": [r["cantidad"] for r in reservas]
        },

        "usuarios": {
            "roles": [r["rol"] for r in usuarios],
            "cantidades": [r["cantidad"] for r in usuarios]
        },

        "reseñas": {
            "aspectos": [
                "Ambiente",
                "Servicio",
                "Comida"
            ],
            "promedios": [
                float(resenas["ambiente"] or 0),
                float(resenas["servicio"] or 0),
                float(resenas["comida"] or 0)
            ]
        },

        "menu": {
            "categorias": [r["nombre"] for r in menu],
            "cantidades": [r["cantidad"] for r in menu]
        }
    }

    return results
