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