from flask import Blueprint, request, jsonify
from api.services import menu as menu_service

menu_bp = Blueprint("menu", __name__)

#Cambiar producto - Flor
@menu_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.get_json()
    updated, code = menu_service.editar_producto(id, data)
    if code == 204:
        return "", code
    return jsonify(updated), code

#Consultar productos - John
@menu_bp.route('/productos', methods=['GET'])
def obtener_productos():
    base_url = request.base_url
    #limit = request.args.get('limit', default=10, type=int)#  
    #offset = request.args.get('offset', default=0, type=int) #
    productos, code = menu_service.ver_productos(base_url) #van limit y offset
    if code == 204:
        return "", code
    return jsonify(productos), code

#Eliminar producto - Nico
@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    
    resultado = elimina_producto(id_producto)

    if resultado == 'id_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif resultado == 'Error_db':
        return jsonify(ReturnErrors(500)), 500
    elif resultado == 'Producto_no_encontrado':
        return jsonify(ReturnErrors(404)), 404
    else:
        return '', 204