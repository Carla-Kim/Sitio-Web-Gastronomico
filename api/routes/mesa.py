from flask import Blueprint, request, jsonify
from api.services import mesa as mesas
from api.utils.errors import ReturnErrors

mesa_bp = Blueprint("mesa", __name__)

@mesa_bp.route("/mesas", methods=["GET"])
def obtener_estado_mesa():
    try:
        datos_disponibles = mesas.disponibilidad_mesas()
        return jsonify(datos_disponibles), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"Error crítico al consultar disponibilidad de mesas: {e}")
        return jsonify(ReturnErrors(500)), 500

@mesa_bp.route("/mesas/<int:mesa_id>", methods=["PUT"])
def update_estado_mesa(mesa_id):
    body = request.get_json()

    if not body or mesa_id <= 0:
        return jsonify(ReturnErrors(400)), 400
    
    try:
        mesas.actualizar_Estado(mesa_id, body)
        return jsonify({"message": "Estado de mesa actualizado exitosamente"}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500

@mesa_bp.route("/mesas", methods=["POST"])
def crear_mesa():
    try:
        nueva_mesa_id = mesas.crear_nueva_mesa()
        return jsonify({
            "status": "success",
            "message": "Mesa creada exitosamente con 2 asientos",
            "mesa_id": nueva_mesa_id
        }), 201
    except Exception as e:
        print(f"Error crítico al crear mesa: {e}")
        return jsonify(ReturnErrors(500)), 500

@mesa_bp.route("/mesas/<int:mesa_id>", methods=["DELETE"])
def eliminar_mesa(mesa_id):
    if mesa_id <= 0:
        return jsonify(ReturnErrors(400)), 400
        
    try:
        mesas.eliminar_mesa(mesa_id)
        return jsonify({"message": f"Mesa {mesa_id} eliminada correctamente"}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"Error crítico al eliminar mesa: {e}")
        return jsonify(ReturnErrors(500)), 500