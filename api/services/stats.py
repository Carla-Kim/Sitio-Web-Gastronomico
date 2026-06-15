from ..database import stats

def obtener_stats():

    # Obtiene la cantidad de reservas agrupadas por estado.
    reservas_estado = stats.obtener_reservas_por_estado()

    # Obtiene la cantidad de reservas agrupadas por mes.
    reservas_mes = stats.obtener_reservas_por_mes()

    # Obtiene la cantidad de productos y el precio promedio por categoría.
    categorias = stats.obtener_productos_por_categoria()

    # Obtiene los promedios de puntuación de las reseñas habilitadas.
    resenas = stats.obtener_promedio_resenas()

    # Obtiene el servicio más solicitado por los clientes.
    servicio_mas_solicitado = stats.obtener_servicio_mas_solicitado()

    meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    results = {

        "reservas_por_estado": {
            "estados": [r["estado"] for r in reservas_estado],
            "cantidades": [r["cantidad"] for r in reservas_estado]
        },

        "reservas_por_mes": {
            "meses": [meses[r["mes"] - 1] for r in reservas_mes],
            "cantidades": [r["cantidad"] for r in reservas_mes]
        },

        "productos_por_categoria": {
            "categorias": [r["nombre"] for r in categorias],
            "cantidades": [r["cantidad"] for r in categorias],
            "precios_promedio": [
                float(r["precio_promedio"] or 0)
                for r in categorias
            ]
        },

        "promedio_resenas": {
            "ambiente": float(resenas["ambiente"] or 0),
            "servicio": float(resenas["servicio"] or 0),
            "comida": float(resenas["comida"] or 0),
            "general": float(resenas["general"] or 0)
        },

        "servicio_mas_solicitado": {
            "nombre": servicio_mas_solicitado["nombre"] if servicio_mas_solicitado else None,
            "cantidad": servicio_mas_solicitado["cantidad"] if servicio_mas_solicitado else 0
        }
    }

    return results
