from flask import Blueprint, request, jsonify

from ..services.usuario import *
from ..utils.errors import *

usuarios_bp = Blueprint('usuarios', __name__)


# Endpoint para listar usuarios
@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    base_url = request.base_url
    query_args = request.args.to_dict()

    limit = request.args.get("_limit", type=int, default=10)
    offset = request.args.get("_offset", type=int, default=0)

    rol = request.args.get("rol")

    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    try:
        results = obtener_usuarios(
            base_url=base_url,
            query_params=query_args,
            limit=limit,
            offset=offset,
            rol=rol
        )

        return jsonify(results), 200

    except ValueError:
        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"No fue posible listar los usuarios. Error: {e}")
        return jsonify(ReturnErrors(500)), 500
    
# Endpoint para buscar usuario por ID
@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    try:
        usuario = obtener_usuario_por_id(id)

        return jsonify(usuario), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"No fue posible obtener el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500
    
# Endpoint para mostrar contraseña por email
@usuarios_bp.route('/usuarios/<string:email>', methods=['GET'])
def mostrar_contrasena(email):
    try:
        contrasena = obtener_contrasena_por_email(email)

        return jsonify(contrasena), 200

    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404

        return jsonify(ReturnErrors(400)), 400

    except Exception as e:
        print(f"No fue posible obtener la contraseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500