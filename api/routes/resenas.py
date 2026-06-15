from flask import Blueprint, request, jsonify
from api.services import resenas as resenas_service
from api.utils.errors import ReturnErrors
from api.utils.formato_fecha import formato_fecha

resenas_bp = Blueprint("resenas", __name__)

@resenas_bp.route('/resenas', methods=['GET'])
def obtener_resenas():
    base_url = request.base_url
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    estado = request.args.get('estado', default=None, type=str)
    fecha_desde = request.args.get('fecha_desde', default=None, type=str)
    fecha_hasta = request.args.get('fecha_hasta', default=None, type=str)

    p_ambiente = request.args.get('puntaje_ambiente', default=None, type=int)
    p_servicio = request.args.get('puntaje_servicio', default=None, type=int)
    p_comida = request.args.get('puntaje_comida', default=None, type=int)

    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    try:
        resultado = resenas_service.listar_resenas(base_url, limit, offset, fecha_desde, fecha_hasta, p_ambiente, p_servicio, p_comida, estado)
        lista_elementos = resultado.get('data', resultado.get('resenas', []))
        conteo_total = resultado.get('count', resultado.get('total', 0))
        formato_fecha(lista_elementos)

        return jsonify({
            "data": lista_elementos,
            "resenas": lista_elementos,
            "count": conteo_total,
            "total": conteo_total
        }), 200
    
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible listar las reseñas. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@resenas_bp.route('/resenas/<int:resena_id>', methods=['GET']) 
def obtener_resena_por_id(resena_id):
    try:
        resultado = resenas_service.buscar_por_id(resena_id)
        if resultado:
            formato_fecha([resultado])
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener la reseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@resenas_bp.route('/resenas/reserva/<int:reserva_id>', methods=['GET'])
def obtener_resena_por_reserva(reserva_id):
    try:
        resultado = resenas_service.buscar_por_reserva(reserva_id)
        if resultado:
            formato_fecha([resultado])
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener la reseña de la reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@resenas_bp.route('/resenas/promedio/<string:columna>', methods=['GET'])
def obtener_promedio_columna(columna):
    if columna not in ['ambiente', 'servicio', 'comida']:
        return jsonify(ReturnErrors(400)), 400
    try:
        columna_db = f"puntuacion_{columna}"
        resultado = resenas_service.obtener_promedio(columna_db)
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener el promedio de {columna}. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@resenas_bp.route('/resenas', methods=['POST'])
def crear_resena():
    if not request.is_json:
        return jsonify(ReturnErrors(415)), 415
        
    data = request.get_json()
    try:
        resultado = resenas_service.crear_resena(data)
        return jsonify(resultado), 201
    except ValueError as val_err:
        error_msg = str(val_err)
        if error_msg == "CONFLICT":
            return jsonify(ReturnErrors(409)), 409
        if error_msg in ["NO_EXISTE", "NOT_FOUND"]:
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible crear la reseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@resenas_bp.route('/resenas/<int:resena_id>', methods=['PATCH'])
def cambiar_estado_resena(resena_id):
    if not request.is_json:
        return jsonify(ReturnErrors(415)), 415
        
    data = request.get_json()
    try:
        resultado = resenas_service.actualizar_estado_resena(resena_id, data)
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible actualizar el estado de la reseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500