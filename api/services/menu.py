import re
from api.database import menu as menu_db
from api.utils.errors import ReturnErrors
from api.utils.pagination import build_links
from api.services.storage import subir_imagen

def ingresar_producto(data, imagen=None):
    imagen_url = None

    if imagen:
        imagen_url = subir_imagen(imagen)

    if not data:
        return ReturnErrors(400), 400
    categorias_id = data.get('categorias_id')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    
    if not all([categorias_id, nombre, descripcion, precio]):
        return ReturnErrors(400), 400
        
    try:
        if menu_db.check_by_nombre(nombre):
            return ReturnErrors(409), 409
            
        nuevo_id = menu_db.ingresar_producto(categorias_id, nombre, descripcion, precio, imagen_url)
        
        resultado = {
            "status": "success",
            "message": "Producto ingresado correctamente.",
            "producto_id": nuevo_id
        }
        return resultado, 201

    except Exception as e:
        print(f"Error interno en servicio menu: {e}") 
        return ReturnErrors(500), 500

def editar_producto(id, data, imagen=None):
    if not data:
        return ReturnErrors(400), 400
    categoria_id = data.get('categorias_id')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    imagen_url = data.get('imagen_url')
    
    if not all([categoria_id, nombre, descripcion, precio]):
        return ReturnErrors(400), 400
    
    try:
        producto = menu_db.check_by_id(id)
        if not producto:
            return ReturnErrors(404), 404

        imagen_url = producto["imagen_url"]
        if imagen:
            imagen_url = subir_imagen(imagen)

        menu_db.editar_producto(id, categoria_id, nombre, descripcion, precio, imagen_url)
        return "", 204

    except Exception:
        return ReturnErrors(500), 500

def ver_productos(base_url, limit, offset, orden= None):
    filtro= "producto_id"
    direccion_filtro = "ASC"

    if orden:
        orden_clear = orden.lower()
        if orden_clear == "min":
            filtro = "precio"
            direccion_filtro = "ASC"
        elif orden_clear == "max":
            filtro = "precio"
            direccion_filtro = "DESC"
        
    try:
        res_db = menu_db.obtener_productos(limit, offset, filtro, direccion_filtro)
    except Exception:
        return ReturnErrors(500), 500
    if not res_db["rows"]:
        return "", 204

    
    productos_mapeados = [{
        "id": d["producto_id"],
        "categoria": d["categorias_id"],
        "nombre": d["nombre"],
        "descripcion": d["descripcion"],
        "precio": d["precio"],
        "imagen_url": d["imagen_url"]
    } for d in res_db["rows"]]

    count = res_db["count"]

    return {
        "productos": productos_mapeados
    }, 200

def elimina_producto(id_producto):
    if id_producto is None:
        return ReturnErrors(400), 400
    
    try:
        resultado = menu_db.borrar_producto(id_producto)
        if resultado == 0:
            return ReturnErrors(404), 404
        return {"message": "Se elimino correctamente"}, 200
    except Exception:
        return ReturnErrors(500), 500

def obtener_producto(nombre):
    if not nombre or nombre.isspace():
        return ReturnErrors(400), 400
    try:
        producto = menu_db.obtener_producto_por_nombre(nombre)
        if producto is None:
            return ReturnErrors(404), 404
        return {"producto": producto}, 200
    except Exception:
        return ReturnErrors(500), 500
