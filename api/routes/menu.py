from flask import Blueprint, request, jsonify
from api.services import menu as menu_service
from api.utils.errors import ReturnErrors

menu_bp = Blueprint("menu", __name__)

@menu_bp.route('/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.form.to_dict()
    imagen = request.files.get("imagen")
    updated, code = menu_service.editar_producto(id, data, imagen)
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
    data = request.form.to_dict()
    imagen = request.files.get("imagen")
    resultado, code = menu_service.ingresar_producto(data, imagen)
    
    return jsonify(resultado), code

@menu_bp.route('/productos/<int:id>', methods=['GET'])
def buscar_producto(id):
    result = menu_service.obtener_producto_por_id(id)
    
    if result == 'producto_no_encontrado':
        return jsonify(ReturnErrors(404)), 404
        
    elif isinstance(result, tuple) and result[0] == 'exito':
        producto_dict = result[1]
        return jsonify(producto_dict), 200
        
    else:
        return jsonify(ReturnErrors(500)), 500

@menu_bp.route('/productos/categoria/<int:categoria_id>', methods=['GET'])
def buscar_productos_por_categoria(categoria_id):
    result = menu_service.obtener_productos_por_categoria(categoria_id)
    
    if result == 'no_encontrado':
        return jsonify({"message": "No se encontraron productos para esta categoría", "data": []}), 200
        
    elif isinstance(result, tuple) and result[0] == 'exito':
        productos_lista = result[1]
        return jsonify(productos_lista), 200
        
    else:
        return jsonify(ReturnErrors(500)), 500