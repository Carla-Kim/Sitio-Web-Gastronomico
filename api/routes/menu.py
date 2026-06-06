from flask import Blueprint, request, jsonify
from api.services import menu as menu_service
from api.utils.errors import ReturnErrors

menu_bp = Blueprint("menu", __name__)

@menu_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.get_json()
    updated, code = menu_service.editar_producto(id, data)
    if code == 204:
        return "", code
    return jsonify(updated), code

@menu_bp.route('/productos', methods=['GET'])
def obtener_productos():
    base_url = request.base_url
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    

    orden = request.args.get('orden', default='producto_id', type=str)

    productos, code = menu_service.ver_productos(base_url, limit, offset, orden)
    if code == 204:
        return "", code
    return jsonify(productos), code

@menu_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    resultado, code = menu_service.elimina_producto(id_producto)
    if code == 204 or code == 200:
        if isinstance(resultado, dict):
            return jsonify(resultado), code
        return "", code
    return jsonify(resultado), code

@menu_bp.route('/productos', methods=['POST'])
def ingresar_producto():
    if not request.is_json:
        return jsonify(ReturnErrors(415)), 415
        
    data = request.get_json()
    resultado, code = menu_service.ingresar_producto(data)
    
    return jsonify(resultado), code
