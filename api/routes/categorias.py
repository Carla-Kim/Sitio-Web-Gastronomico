from flask import Blueprint, request, jsonify
from ..services.categorias import *
from ..utils.errors import *

categorias_bp = Blueprint('categorias', __name__)

#Endpoint para update categoría
@categorias_bp.route('/categorias/<int:id>', methods=['PUT'])
def formatear_categoria(id):
    data = request.get_json()

    result = actualizar_categoria(id, data)

    if result == 'body_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    elif result == 'categoria_no_encontrada':
        return jsonify(ReturnErrors(404)), 404
    else:
        return '', 204
    

#Endpoint para agregar categoría
@categorias_bp.route('/categorias', methods=['POST']) 
def agregar_categoria():
    data = request.get_json()
    result = crear_categoria(data)
    if result == 'body_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif result == 'nombre_duplicado':
        return jsonify(ReturnErrors(409)), 409 
    elif result == 'error_db':
        return jsonify(ReturnErrors(500)), 500
    else:
        return jsonify({'message': 'Categoría creada con éxito'}), 201

    

