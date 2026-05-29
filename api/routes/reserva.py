from flask import Blueprint, request, jsonify
from ..services.reservas import *
from ..utils.errors import *

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['POST'])
def agregar_reserva():
    data = request.get_json()
    result = crear_reserva(data)
    
    if result == 'body_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'estado_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'cantidad_invalida':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'reserva_duplicada':
        return jsonify(ReturnErrors(409)), 409
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        return jsonify({'message': 'Reserva creada con éxito'}), 201

@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def formatear_reserva(id):
    data = request.get_json()
    result = actualizar_reserva(id, data)

    if result == 'body_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'estado_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'cantidad_invalida':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    elif result == 'reserva_no_encontrada':
        return jsonify(ReturnErrors(404)), 404
    else:
        return '', 204

@reservas_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    base_url = request.base_url
    query_args = request.args.to_dict()
    
    limit = request.args.get("_limit", type=int, default=10)
    offset = request.args.get("_offset", type=int, default=0)
    
    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    try:
        results = obtener_reservas(base_url, query_args, limit, offset)
        return jsonify(results), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500
    
@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def buscar_reserva(id):
    result = obtener_reserva_por_id(id)
    
    if result == 'reserva_no_encontrada':
        return jsonify(ReturnErrors(404)), 404
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        status, reserva = result
        return jsonify(reserva), 200