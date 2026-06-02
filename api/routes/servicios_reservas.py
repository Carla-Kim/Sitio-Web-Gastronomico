from flask import Blueprint, request, jsonify
from ..services import servicios_reservas as sr
from ..utils.errors import ReturnErrors

servicio_reserva_bp = Blueprint('servicio_reserva', __name__)

@servicio_reserva_bp.route('/servicios-reservas', methods=['GET'])
def listar_servicios_reserva():
    try:
        results = sr.obtener_servicios_reserva()
        return jsonify(results), 200
    except ValueError:
        return jsonify(ReturnErrors(404)), 404
    except Exception as e:
        print(f"No fue posible listar servicios_reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@servicio_reserva_bp.route('/servicios-reservas/<int:reserva_id>', methods=['GET'])
def listar_servicios_por_reserva(reserva_id):
    try:
        results = sr.obtener_servicios_por_reserva(reserva_id)
        return jsonify(results), 200
    except ValueError:
        return jsonify(ReturnErrors(404)), 404
    except Exception as e:
        print(f"No fue posible listar servicios de la reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@servicio_reserva_bp.route('/servicios-reservas/<int:reserva_id>', methods=['PUT'])
def modificar_servicio_reserva(reserva_id):
    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        sr.asociar_servicios_reserva(reserva_id, body)
        return jsonify({"message": "Servicios asociados correctamente"}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        if str(val_err) == "CONFLICT":
            return jsonify(ReturnErrors(409)), 409
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible asociar servicios a la reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@servicio_reserva_bp.route('/servicios-reservas/<int:reserva_id>', methods=['DELETE'])
def borrar_servicio_reserva(reserva_id):
    try:
        sr.eliminar_servicios_reserva(reserva_id)
        return '', 204
    except ValueError:
        return jsonify(ReturnErrors(404)), 404
    except Exception as e:
        print(f"No fue posible eliminar servicios de la reserva. Error: {e}")
        return jsonify(ReturnErrors(500)), 500