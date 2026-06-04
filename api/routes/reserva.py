from flask import Blueprint, request, jsonify
from api.services import reserva as reservas_service
from api.utils.errors import ReturnErrors

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['POST'])
def agregar_reserva():
    data = request.get_json()
    result = reservas_service.crear_reserva(data)
    
    if result == 'body_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'email_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'dni_invalido':
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
    result = reservas_service.actualizar_reserva(id, data)

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
        results = reservas_service.obtener_reservas(base_url, query_args, limit, offset)
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
    result = reservas_service.obtener_reserva_por_id(id)
    
    if result == 'reserva_no_encontrada':
        return jsonify(ReturnErrors(404)), 404
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        status, reserva = result
        return jsonify(reserva), 200
    
@reservas_bp.route('/reservas/estado/<string:estado>', methods=['GET'])
def listar_reservas_por_estado(estado):
    base_url = request.base_url
    query_args = request.args.to_dict()
    
    limit = request.args.get("_limit", type=int, default=10)
    offset = request.args.get("_offset", type=int, default=0)
    
    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    result = reservas_service.filtrar_por_estado(base_url, query_args, estado, limit, offset)
    if result == 'estado_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'no_encontrado':
        return jsonify(ReturnErrors(404)), 404
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        status, response_body = result
        return jsonify(response_body), 200
    
@reservas_bp.route('/reservas/fecha/<string:fecha>', methods=['GET'])
def listar_reservas_por_fecha(fecha):
    base_url = request.base_url
    query_args = request.args.to_dict()
    
    limit = request.args.get("_limit", type=int, default=10)
    offset = request.args.get("_offset", type=int, default=0)
    
    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    result = reservas_service.obtener_reservas_por_fecha(base_url, query_args, fecha, limit, offset)

    if result == 'fecha_invalida':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'no_encontrado':
        return jsonify(ReturnErrors(404)), 404
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        status, response_body = result
        return jsonify(response_body), 200
    
@reservas_bp.route('/reservas/<int:id>/cancelar', methods=['PATCH'])
def cancelar_reserva_endpoint(id):
    result = reservas_service.cancelar_reserva(id)

    if result == 'id_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'reserva_no_encontrada':
        return jsonify(ReturnErrors(404)), 404
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        status, response_body = result
        return jsonify(response_body), 200
