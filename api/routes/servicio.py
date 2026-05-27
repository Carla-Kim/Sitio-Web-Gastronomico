from flask import Blueprint, request, jsonify

from api.services.servicio import *
from api.utils.errors import *

servicio_br = Blueprint("servicio", __name__)

#Endpoint para listar servicios
@servicio_br.route("/servicios", methods=["GET"])
def lista_servicios():
    base_url = request.base_url
    query_args = request.args.to_dict()

    limit = request.args.get('limit', default=10, type=int) 
    offset = request.args.get('offset', default=0, type=int) 

    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400
    
    try:
        resultado = ver_servicios(base_url, query_args, limit, offset)
        return jsonify(resultado), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"Error crítico capturado en la ruta: {e}")
        return jsonify(ReturnErrors(500)), 500