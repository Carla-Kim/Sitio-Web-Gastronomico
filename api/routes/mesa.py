from flask import Blueprint, request, jsonify
from api.services.mesa import *
from api.utils.errors import *

mesa_br = Blueprint("mesa", __name__)

#Endpoint para consultar la cantidad de mesas disponibles
@mesa_br.route("/mesas", methods=["GET"])
def obtener_estado_mesa():
    try:
        datos_disponibles = disponibilidad_mesas()
        return jsonify(datos_disponibles), 200
    except ValueError as val_err:
        
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico al consultar disponibilidad de mesas: {e}")
        return jsonify(ReturnErrors(500)), 500


#Endpoint para cambiar el estado de una mesa (ocupada/desocupada)
@mesa_br.route("/mesa/<int:mesa_id>", methods=["PUT"])
def update_estado_mesa(mesa_id):
    body = request.get_json()

    if not body or mesa_id <= 0:
        return jsonify(ReturnErrors(400)), 400
    
    try:
        actualizar_Estado(mesa_id, body)
        return jsonify({"message": "Estado de mesa actualizado exitosamente"}), 200
    
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500