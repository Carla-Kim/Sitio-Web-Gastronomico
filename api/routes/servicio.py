from flask import Blueprint, request, jsonify
from api.services import servicio as servicios
from api.utils.errors import *

servicio_bp = Blueprint("servicio", __name__)

#Endpoint para listar servicios.
@servicio_bp.route("/servicios", methods=["GET"])
def lista_servicios():
    base_url = request.base_url
    query_args = request.args.to_dict()

    limit = request.args.get('limit', default=10, type=int) 
    offset = request.args.get('offset', default=0, type=int) 

    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400
    
    try:
        resultado = servicios.ver_servicios(base_url, query_args, limit, offset)
        return jsonify(resultado), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500

#Endpoint para obtener un servicio por estado.    
@servicio_bp.route("/servicios/estado/<string:estado>", methods=["GET"])
def servicios_por_estado(estado):

    try:
        resultado = servicios.ver_servicios_estado(estado)
        return jsonify(resultado), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500

#Endpoint para obtener un servicio por ID.
@servicio_bp.route("/servicios/<int:servicio_id>", methods=["GET"])
def servicio_id(servicio_id):

    try:
        resultado = servicios.ver_servicio_id(servicio_id)
        return jsonify(resultado), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500
    

#Endpoint para crear un nuevo servicio.
@servicio_bp.route("/servicios", methods=["POST"])
def crear_new_servicio():
    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        new_servicio = servicios.crear_servicio(body)
        return jsonify(new_servicio), 201
    
    except ValueError as val_err:
        if str(val_err) == "CONFLICT":
            return jsonify(ReturnErrors(409)), 409
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500
    

# Endpoint para actualizar el nombre de un servicio existente.
@servicio_bp.route("/servicios/<int:servicio_id>/nombre", methods=["PATCH"])
def actualizar_nombre_servicio(servicio_id):
    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        servicios.actualizar_nombre_servicio(servicio_id, body)

        return jsonify({
            "message": "Nombre del servicio actualizado exitosamente"
        }), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        if str(val_err) == "CONFLICT":
            return jsonify(ReturnErrors(409)), 409

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500

# Endpoint para cambiar el estado de un servicio.
@servicio_bp.route("/servicios/<int:servicio_id>/estado", methods=["PATCH"])
def actualizar_estado_servicio(servicio_id):
    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        servicios.actualizar_estado_servicio(servicio_id, body)

        return jsonify({
            "message": "Estado del servicio actualizado exitosamente"
        }), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500