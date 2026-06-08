from flask import Blueprint, request, jsonify
from ..services import usuario as user
from ..utils.errors import ReturnErrors

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    base_url = request.base_url
    query_args = request.args.to_dict()

    limit = request.args.get("limit", type=int, default=10)
    offset = request.args.get("offset", type=int, default=0)
    rol = request.args.get("rol")

    if limit <= 0 or offset < 0:
        return jsonify(ReturnErrors(400)), 400

    try:
        results = user.obtener_usuarios(
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

@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    try:
        usuario = user.obtener_usuario_por_id(id)
        return jsonify(usuario), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/credenciales', methods=['POST'])
def mostrar_contrasena():
    body = request.get_json()
    if not body or 'email' not in body:
        return jsonify(ReturnErrors(400)), 400
    try:
        contrasena = user.obtener_contrasena_por_email(body['email'])
        return jsonify(contrasena), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener la contraseña. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/rol', methods=['POST'])
def mostrar_rol():
    body = request.get_json()
    if not body or 'email' not in body:
        return jsonify(ReturnErrors(400)), 400
    try:
        rol = user.obtener_rol_por_email(body['email'])
        return jsonify(rol), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener el rol del usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    body = request.get_json()
    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        nuevo_usuario = user.crear_nuevo_usuario(body)
        return jsonify(nuevo_usuario), 201
    except ValueError as val_err:
        if str(val_err) == "CONFLICT":
            return jsonify(ReturnErrors(409)), 409
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible crear el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def modificar_usuario(id):
    body = request.get_json()
    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        user.actualizar_usuario(id, body)
        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible actualizar el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/<int:id>', methods=['PATCH'])
def modificar_usuario_parcial(id):
    body = request.get_json()
    if not body:
        return jsonify(ReturnErrors(400)), 400

    try:
        user.actualizar_usuario_parcial(id, body)
        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible actualizar el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def borrar_usuario(id):
    try:
        user.eliminar_usuario(id)
        return '', 204
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible eliminar el usuario. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/email', methods=['GET'])
def obtener_usuario_por_email_route():
    email = request.args.get('email')
    
    if not email or email.isspace():
        return jsonify(ReturnErrors(400)), 400
        
    try:
        usuario = user.obtener_usuario_por_email_servicio(email)
        return jsonify({"usuario": usuario}), 200
    except ValueError as val_err:
        if str(val_err) == "NOT_FOUND":
            return jsonify(ReturnErrors(404)), 404
        return jsonify(ReturnErrors(400)), 400
    except Exception as e:
        print(f"No fue posible obtener el usuario por email. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

@usuarios_bp.route('/usuarios/rol', methods=['GET'])
def obtener_usuarios_por_rol_route():
    rol = request.args.get('rol')
    try:
        limit = int(request.args.get('_limit', default=10))
        offset = int(request.args.get('_offset', default=0))
    except ValueError:
        return jsonify(ReturnErrors(400)), 400
    
    try:
        resultado = user.listar_usuarios_por_rol_servicio(rol, limit, offset)
        base_url = f"http://127.0.0.1:5000/api/usuarios/rol?rol={rol}"
        
        ultimo_offset = max(0, resultado['count'] - limit)
        
        respuesta = {
            "_links": {
                "_first": {
                    "href": f"{base_url}&_limit={limit}&_offset=0"
                },
                "_last": {
                    "href": f"{base_url}&_limit={limit}&_offset={ultimo_offset}"
                }
            },
            "count": resultado["count"], 
            "data": resultado["data"]   
        }
        
        return jsonify(respuesta), 200
        
    except ValueError as val_err:
        if str(val_err) == "BAD_REQUEST":
            return jsonify(ReturnErrors(400)), 400
        return jsonify(ReturnErrors(404)), 404
        
    except Exception as e:
        print(f"Error crítico en filtro por rol: {e}")
        return jsonify(ReturnErrors(500)), 500