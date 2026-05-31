from flask import Blueprint, request, jsonify
from api.services import resenas as resenas_service
from api.utils.errors import ReturnErrors

resenas_bp = Blueprint("resenas", __name__)

# Endpoint para listar reseñas
@resenas_bp.route('/resenas', methods=['GET'])
def obtener_resenas():
    base_url = request.base_url
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)
    
    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    try:
        resultado = resenas_service.listar_resenas(base_url, limit, offset)
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible listar las reseñas. Error: {e}")
        return jsonify(ReturnErrors(500)), 500


# Endpoint para buscar por ID
@resenas_bp.route('/resenas/<int:resena_id>', methods=['GET']) 
def obtener_resena_por_id(resena_id):
    try:
        resultado = resenas_service.buscar_por_id(resena_id)
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener la reseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500


# Endpoint para buscar por reserva
@resenas_bp.route('/resenas/reserva/<int:reserva_id>', methods=['GET'])
def obtener_resena_por_reserva(reserva_id):
    try:
        resultado = resenas_service.buscar_por_reserva(reserva_id)
        return jsonify(resultado), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener la reseña de la reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500


# Endpoint para promedios
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


# Endpoint para crear reseña
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


# Endpoint para borrar reseña
@resenas_bp.route('/resenas/<int:resena_id>', methods=['DELETE']) 
def borrar_resena(resena_id):                                    
    try:
        resenas_service.eliminar_resena(resena_id)
        return "", 204
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible eliminar la reseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500