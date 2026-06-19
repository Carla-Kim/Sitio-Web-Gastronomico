from flask import Blueprint, request, jsonify
from api.services import mesa as mesas
from api.utils.errors import ReturnErrors

mesa_bp = Blueprint("mesa", __name__)

# Endpoint para obtener la cantidad de mesas ocupadas y desocupadas.
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


# Endpoint para actualizar la cantidad de mesas de un estado.
@mesa_bp.route("/mesas/<string:estado>", methods=["PATCH"])
def actualizar_cantidad_mesas(estado):
    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        mesas.actualizar_cantidad_mesas(estado, body)
        return jsonify({
            "message": "Cantidad de mesas actualizada exitosamente"
        }), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500

# Endpoint para actualizar la capacidad total de mesas del local.
@mesa_bp.route("/mesas/capacidad", methods=["PATCH"])
def actualizar_capacidad_local():

    body = request.get_json()

    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:

        mesas.actualizar_capacidad_local(body)

        return jsonify({
            "message": "Capacidad de mesas actualizada exitosamente"
        }), 200

    except ValueError as val_err:

        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500
