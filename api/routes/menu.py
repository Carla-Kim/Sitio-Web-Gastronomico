from flask import Blueprint, request, jsonify
from api.services import menu as menu_service
from api.utils.errors import ReturnErrors  # Subimos el import de errores para que lo usen todos

menu_bp = Blueprint("menu", __name__)

# Cambiar producto - Flor
@menu_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.get_json()
    updated, code = menu_service.editar_producto(id, data)
    if code == 204:
        return "", code
    return jsonify(updated), code

# Consultar productos - John
@menu_bp.route('/productos', methods=['GET'])
def obtener_productos():
    base_url = request.base_url
    productos, code = menu_service.ver_productos(base_url)
    if code == 204:
        return "", code
    return jsonify(productos), code

# Eliminar producto - Nico
@menu_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    
    resultado = menu_service.elimina_producto(id_producto) 

    if resultado == 'id_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif resultado == 'Error_db':
        return jsonify(ReturnErrors(500)), 500
    elif resultado == 'Producto_no_encontrado':
        return jsonify(ReturnErrors(404)), 404
    else:
        return '', 204

# Ingresar producto - Neithan
@menu_bp.route('/productos', methods=['POST'])
def ingresar_producto():
    if not request.is_json:
        return jsonify(ReturnErrors(415)), 415
        
    data = request.get_json()
    resultado, code = menu_service.ingresar_producto(data)
    
    return jsonify(resultado), code