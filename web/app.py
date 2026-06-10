import os
import sys
import requests
from functools import wraps
from api.app import app as api_app
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
API_URL = os.getenv("API_URL", "http://localhost:5000/api")
SECRET_KEY = os.getenv("SECRET_KEY", "basheros123")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = SECRET_KEY


def login_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get("usuario_id") is None:
            return redirect('/dashboard/login')

        return view(*args, **kwargs)

    return wrapper


@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    try:
        resp = requests.get('http://localhost:5000/api/servicios')
        servicios = resp.json().get('data', []) if resp.status_code == 200 else []
    except:
        servicios = []
    
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre', '').split(' ', 1)
        nombre = nombre_completo[0]
        apellido = nombre_completo[1] if len(nombre_completo) > 1 else ''

        comensales_form = request.form.get('comensales') or '0'

        data = {
            "cantidad_personas": int(comensales_form),
            "fecha": request.form.get('fecha'),
            "nombre": nombre,
            "apellido": apellido,
            "email": request.form.get('email'),
            "DNI": request.form.get('documento'),
            "telefono": request.form.get('telefono'),
        }

        try:
            response = requests.post('http://localhost:5000/api/reservas', json=data)

            if response.status_code == 201:
                reserva_id = response.json().get('reserva_id')
                serv_seleccionados = request.form.getlist('servicios')

                if serv_seleccionados and reserva_id:
                    requests.put(f'http://localhost:5000/api/servicios-reservas/{reserva_id}', json ={"servicios_id": [int(s) for s in serv_seleccionados]})
                flash('Se realizó la reserva con exito.', 'success')
                return redirect(url_for('reservas'))
            else:
                error_msg = response.json().get('errors', [{}])[0].get('message', 'Ha ocurrido un error inesperado')
                flash(error_msg, 'error')
        
        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            flash('Error de conexión.', 'error')

    return render_template('reservas.html', servicios=servicios)

@app.route('/menu', endpoint='menu')
def mostrar_menu():
    with api_app.test_client() as client:
        categorias_resp = client.get('/categorias', query_string={'_limit': 1000, '_offset': 0})
        productos_resp = client.get('/productos', query_string={'limit': 1000, 'offset': 0})

    if categorias_resp.status_code != 200 or productos_resp.status_code != 200:
        return render_template('menu.html', menu_agrupado=[])

    categorias_data = categorias_resp.get_json().get('data', [])
    productos_data = productos_resp.get_json().get('productos', [])

    menu_agrupado = []
    for categoria in categorias_data:
        cat_id = categoria.get('categorias_id', categoria.get('id'))
        
        productos_filtrados = [
            p for p in productos_data 
            if p.get('categoria') == cat_id
        ]
        
        menu_agrupado.append({
            'categoria': categoria,
            'productos': productos_filtrados
        })

    return render_template('menu.html', menu_agrupado=menu_agrupado)

@app.route('/resenas')
def resenas():       
    limit = request.args.get('limit', default=3, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    with api_app.test_client() as client:
        resenas_resp = client.get('/resenas', query_string={'limit': limit, 'offset': offset})
        promedio_ambiente_resp = client.get('/resenas/promedio/ambiente')
        promedio_comida_resp = client.get('/resenas/promedio/comida')
        promedio_servicio_resp = client.get('/resenas/promedio/servicio')
    
    resenas_list = []
    total_resenas = 0
    promedio_ambiente = 0
    promedio_comida = 0
    promedio_servicio = 0
    
    if resenas_resp.status_code == 200:
        resenas_data = resenas_resp.get_json()
        resenas_list = resenas_data.get('resenas', [])
        
        if 'total' in resenas_data:
            raw_total = resenas_data['total']
        elif 'count' in resenas_data:
            raw_total = resenas_data['count']
        else:
            raw_total = 0

        if isinstance(raw_total, dict):
            total_resenas = raw_total.get('count', raw_total.get('total', 0))
        elif isinstance(raw_total, (list, tuple)):
            total_resenas = raw_total[0] if raw_total else 0
        else:
            try:
                total_resenas = int(raw_total)
            except (ValueError, TypeError):
                total_resenas = len(resenas_list)
                
    if promedio_ambiente_resp.status_code == 200:
        promedio_ambiente = promedio_ambiente_resp.get_json().get('promedio', 0)
    if promedio_comida_resp.status_code == 200:
        promedio_comida = promedio_comida_resp.get_json().get('promedio', 0)
    if promedio_servicio_resp.status_code == 200:
        promedio_servicio = promedio_servicio_resp.get_json().get('promedio', 0)
    
    total_paginas = (total_resenas + limit - 1) // limit if total_resenas > 0 else 1
    pagina_actual = (offset // limit) + 1
    
    return render_template('resenas.html', 
                          resenas=resenas_list,
                          promedio_ambiente=promedio_ambiente,
                          promedio_comida=promedio_comida,
                          promedio_servicio=promedio_servicio,
                          limit=limit,
                          offset=offset,
                          total_paginas=total_paginas,
                          pagina_actual=pagina_actual)

@app.route('/calificar', methods=['GET', 'POST'])
def calificar():
    if request.method == 'GET':
        reserva_id = request.args.get('reserva_id', type=int)

        if reserva_id is None:
            flash('El enlace no es válido', 'error')
            return render_template('dejar-resena.html', reserva_id=None)
        
        response = requests.get(f'http://localhost:5000/api/resenas/reserva/{reserva_id}')

        if response.status_code == 200:
            return render_template('resena-enviada.html')
        return render_template('dejar-resena.html', reserva_id=reserva_id)
    
    reserva_id= request.form.get('reserva_id', type=int)

    data = {
        'reserva_id':       reserva_id,
        'puntaje_ambiente': request.form.get('ambiente', type=int),
        'puntaje_servicio': request.form.get('servicio', type=int),
        'puntaje_comida':   request.form.get('comida', type=int),
        'comentario':       request.form.get('comentarios', '').strip() or None,
    }

    try:
        response = requests.post('http://localhost:5000/api/resenas', json=data)
        if response.status_code == 201:
            return redirect(url_for('resena_enviada', reserva_id=reserva_id))
        
        if response.status_code == 409:
            flash('Ya existe una reseña para esta reserva.', 'error')
        elif response.status_code == 404:
            flash('No se encontró la reserva.', 'error')
        else:
            flash('Ha ocurrido un error', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('calificar', reserva_id=reserva_id))

@app.route('/resena-enviada')
def resena_enviada():
    reserva_id = request.args.get('reserva_id', type=int)

    if reserva_id is None:
        return redirect(url_for('index'))
    
    return render_template('resena-enviada.html', reserva_id=reserva_id)

@app.route('/dashboard')
@login_requerido
def dashboard_home():
    response = requests.get(f"{API_URL}/stats")
    stats = response.json()

    return render_template(
        "dashboard-home.html",
        stats=stats
    )

@app.route('/dashboard/login', methods=['GET', 'POST'])
def dashboard_login():
    if request.method == 'GET':
        return render_template('dashboard-login.html')

    email = request.form.get('email')
    contraseña = request.form.get('contraseña')

    respuesta = requests.post(
        f'{API_URL}/login',
        json={
            'email': email,
            'contraseña': contraseña
        }
    )

    if respuesta.status_code != 200:
        return redirect(url_for('dashboard_login'))

    datos = respuesta.json()
    session['usuario_id'] = datos['usuario_id']

    return redirect('/dashboard')

@app.route('/dashboard/logout')
def logout():
    session.clear()
    return redirect('/dashboard/login')


@app.route('/dashboard/reservas', methods=['GET', 'POST'])
def dashboard_reservas():  
    if request.method == 'POST':
        id_reserva = request.form.get('reserva_id')
        if not id_reserva:
            flash("No se pudo completar la acción: ID inexistente")
            return redirect(url_for('dashboard_reservas'))
        
        try:
            url_api = f'http://localhost:5000/api/reservas/{id_reserva}/cancelar'
            response = requests.patch(url_api, timeout=5)
            response.raise_for_status()
            flash("Reserva cancelada con éxito")

            return redirect(url_for('dashboard_reservas'))
        
        except requests.exceptions.RequestException as e:
            flash(f"Error en la operación: Tal vez ya fue cancelada.")
            return redirect(url_for('dashboard_reservas'))
       
    estado = request.args.get('estado')
    fecha = request.args.get('fecha')
    id_buscado = request.args.get('id')

    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        limit, offset = 10, 0


    try:
        lista_servicios = []
        lista_servicios_reserva = []
        params = {'_limit': limit, '_offset': offset}
        
        if id_buscado:
            url_api = f'http://localhost:5000/api/reservas/{id_buscado}'
            response = requests.get(url_api, timeout=5)
            response.raise_for_status()
            data = response.json()
            lista_reservas = [data[1]]
            
            url_rel = f'http://localhost:5000/api/servicios-reservas/{id_buscado}'
            resp_rel = requests.get(url_rel, timeout=5)
            if resp_rel.status_code == 200:
                lista_servicios_reserva = resp_rel.json()
        
        elif estado:
            url_api = f'http://localhost:5000/api/reservas/estado/{estado}'
            response = requests.get(url_api, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                data = data[1]
            lista_reservas = data[1] if isinstance(data, list) else data.get('data', [])
            
        elif fecha:
            url_api = f'http://localhost:5000/api/reservas/fecha/{fecha}'
            response = requests.get(url_api, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                data = data[1]
            lista_reservas = data if isinstance(data, list) else data.get('data', [])
            
        else:
            url_api = 'http://localhost:5000/api/reservas'
            response = requests.get(url_api, params=params, timeout=5)
            response.raise_for_status()
            lista_reservas = response.json().get('data', [])
        try:
            response = requests.get('http://localhost:5000/api/servicios', timeout=5)
            response.raise_for_status()
            lista_servicios = response.json().get('data', [])
            dict_servicios = {s['servicio_id']: s['nombre'] for s in lista_servicios}

            for reserva in lista_reservas:
                reserva_id = reserva.get('reserva_id')
                if reserva_id:
                    try:
                    # Llamamos a tu endpoint que trae los servicios de la reserva
                        url_rel = f'http://localhost:5000/api/servicios-reservas/{reserva_id}'
                        resp_rel = requests.get(url_rel, timeout=2)
                        print(f"DEBUG: Consultando {url_rel} -> Status: {resp_rel.status_code}")
                        if resp_rel.status_code == 200:
                            servicios_data = resp_rel.json()
                            nombres = []
                            for item in servicios_data:
                               s_id = item.get('servicio_id')
                               nombres.append(dict_servicios.get(s_id, "Desconocido"))
                            reserva['servicios_str'] = ", ".join(nombres)
                        else:
                            reserva['servicios_str'] = "Ninguno"
                    except:
                        reserva['servicios_str'] = "Error al cargar"

        except requests.exceptions.RequestException:
            flash("Error al ver servicios")
        
        return render_template('dashboard-reservas.html', reservas=lista_reservas, limit=limit, offset=offset, servicios=lista_servicios, servicios_reserva=lista_servicios_reserva)
    except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los criterios seleccionados.")
            return redirect(url_for('dashboard_reservas'))
    except requests.exceptions.RequestException as e:
        print(f"Error crítico: {e}")
        return render_template('error-conexion.html'), 500


@app.route('/dashboard/servicios/crear', methods=['POST'])
def crear_servicio():
    datos = {
        "nombre": request.form.get('nombre')
    }
    try:
        url_api = f'http://localhost:5000/api/servicios'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Servicio creado con éxito")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            flash("Error: Ya existe un servicio con ese nombre.")
        else:
            flash("Error al procesar la solicitud.")
    except requests.exceptions.RequestException:
        flash("Error al crear el servicio")
    return redirect(url_for('dashboard_reservas'))

@app.route('/dashboard/servicios/editar', methods=['POST'])
def editar_servicio():
    id_servicio = request.form.get('servicio_id')
    nuevo_nombre = request.form.get('nombre')

    if not id_servicio or not nuevo_nombre:
        flash("Datos incompletos para la edición.")
        return redirect(url_for('dashboard_reservas'))
    
    try:
        url_api = f'http://localhost:5000/api/servicios/{id_servicio}'
        response = requests.put(url_api, json={"nombre": nuevo_nombre}, timeout=5)
        response.raise_for_status()
        flash("Servicio actualizado con éxito")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            flash("Error: Ya existe otro servicio con ese nombre.")
        else:
            flash("Error al actualizar el servicio.")

    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el servicio")

    return redirect(url_for('dashboard_reservas'))

@app.route('/dashboard/servicios/eliminar', methods=['POST'])
def eliminar_servicio():
    id_servicio = request.form.get('servicio_id')
    try:
        url_api = f'http://localhost:5000/api/servicios/{id_servicio}'
        response = requests.delete(url_api, timeout=5)
        response.raise_for_status()
        flash("Servicio eliminado con éxito")
    except requests.exceptions.RequestException:
        flash("Error al eliminar el servicio")
    return redirect(url_for('dashboard_reservas'))


@app.route('/dashboard/resenas', methods=['GET', 'POST'])
# @login_requerido
def dashboard_resenas():
    if request.method == 'POST':
       resena_a_eliminar = request.form.get('id_resena')
       if not resena_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_resenas'))
       try:
            url_api = f'http://localhost:5000/api/resenas/{resena_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            flash("Reseña eliminada con éxito")
            return redirect(url_for('dashboard_resenas'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
        id_buscado = request.args.get('resena-id')
        id_reserva_buscada = request.args.get('resena-reserva-id')
        try:        
            _limit = int(request.args.get('_limit', 10))  
            _offset = int(request.args.get('_offset', 0))  
        except ValueError:
            _limit, _offset = 10, 0

        try:
            if id_buscado:
                url_api = f'http://localhost:5000/api/resenas/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]
                print(lista_resenas)

            elif id_reserva_buscada:
                url_api = f'http://localhost:5000/api/resenas/reserva/{id_reserva_buscada}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]
                print(lista_resenas)

            else:
                params = {'_limit': _limit, '_offset': _offset}
                url_api = f'http://localhost:5000/api/resenas'
                response = requests.get(url_api, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                print(f"DATA:  {data}")
                lista_resenas = data if isinstance(data, list) else data.get('resenas', [])
            print(f"RESEÑAS: {lista_resenas}")

            return render_template('dashboard-resenas.html', resenas=lista_resenas, _limit=int(_limit), _offset=int(_offset))
       
        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los filtros aplicados.")
            return redirect(url_for('dashboard_resenas'))
        except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500


@app.route('/dashboard/menu', methods=['GET', 'POST'])
# @login_requerido
def dashboard_menu():
    if request.method == 'POST':
       tipo = request.form.get('tipo')
       id_a_eliminar = request.form.get('id')
       if not id_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_menu'))
       try:
            if tipo == 'producto':
                url_api = f'http://localhost:5000/api/productos/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Producto eliminado con éxito")

               

            else:
                url_api = f'http://localhost:5000/api/categorias/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Categoria eliminada con éxito")

               

       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
       return redirect(url_for('dashboard_menu'))
    else:
        nombre_buscado = request.args.get('nombre_buscado')

        try:
            limit = int(request.args.get('limit', 10))
            offset = int(request.args.get('offset', 0))
        except ValueError:
            limit, offset = 10, 0
           
        try:
            # Petición a categorías
            url_api_categorias = 'http://localhost:5000/api/categorias'
            response_categorias = requests.get(url_api_categorias, timeout=5)
            response_categorias.raise_for_status()
            # Aseguramos capturar la lista de categorías correctamente
            lista_categorias = response_categorias.json().get('data', [])

            # Petición a productos
            params = {'limit': limit, 'offset': offset}
            if nombre_buscado:
                params['nombre'] = nombre_buscado
                url_productos = 'http://localhost:5000/api/productos/obtener'
                response_productos = requests.get(url_productos, params=params, timeout=5)
                response_productos.raise_for_status()
                data = response_productos.json()
                lista_productos = data.get('productos', [])
            else:
                url_productos = 'http://localhost:5000/api/productos'
                response_productos = requests.get(url_productos, params=params, timeout=5)
                response_productos.raise_for_status()
                data = response_productos.json()
                lista_productos = data.get('productos', [])
            
            print("DEBUG: Lista de productos recibida:", [p['nombre'] for p in lista_productos])
            return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias)
        
        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los filtros aplicados.")
            return redirect(url_for('dashboard_menu'))

        except requests.exceptions.RequestException as e:
            print(f"Error crítico en dashboard_menu: {e}")
            return render_template('error-conexion.html'), 500
       
@app.route('/dashboard/menu/crear', methods=['POST'])
def crear_producto():
    try:
        precio = float(request.form.get('precio', 0))
        categorias_id = int(request.form.get('categorias_id', 0))
    except (ValueError, TypeError):
        print("Datos recibidos en el form:", request.form)
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu'))
    datos = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": precio,
        "categorias_id": categorias_id
    }
    
    try:
        url_api = f'http://localhost:5000/api/productos'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Producto creado con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al crear el producto")
    return redirect(url_for('dashboard_menu'))

@app.route('/dashboard/menu/editar', methods=['POST'])
def editar_producto():
    id_producto = request.form.get('id')
    try:
        precio = float(request.form.get('precio', 0))
        categorias_id = int(request.form.get('categorias_id', 0))
    except (ValueError, TypeError):
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu'))
    datos = {
        "categorias_id": categorias_id,
        "nombre": request.form.get('nombre'),
        "precio": precio,
        "descripcion": request.form.get('descripcion')
    }

    try:
        url_api = f'http://localhost:5000/api/productos/{id_producto}'
        response = requests.put(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Producto actualizado con éxito")
    except requests.exceptions.RequestException:
        flash("Error al actualizar el producto")
    return redirect(url_for('dashboard_menu'))

@app.route('/dashboard/categorias/crear', methods=['POST'])
def crear_categoria():
    datos = {
        "nombre": request.form.get('nombre_categoria')
    }
    try:
        url_api = f'http://localhost:5000/api/categorias'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Categoría creada con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al crear la categoría")
    return redirect(url_for('dashboard_menu'))

@app.route('/dashboard/categorias/editar', methods=['POST'])
def editar_categoria():
    id_categoria = request.form.get('id')
    datos = {"nombre": request.form.get('nombre')}
    try:
        url_api = f'http://localhost:5000/api/categorias/{id_categoria}'
        response = requests.put(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Categoría actualizada con éxito")
    except requests.exceptions.RequestException:
        flash("Error al actualizar la categoría")
    return redirect(url_for('dashboard_menu'))

       
@app.route('/dashboard/usuarios', methods=['GET', 'POST'])
# @login_requerido
def dashboard_usuarios():
    if request.method == 'POST':
       usuario_a_eliminar = request.form.get('id_usuario')
       if not usuario_a_eliminar:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_usuarios'))
       try:
            url_api = f'http://localhost:5000/api/usuarios/{usuario_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
            flash("Se elimino correctamente.")
            return redirect(url_for('dashboard_usuarios'))
       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
        id_buscado = request.args.get('id')
        email_buscado = request.args.get('email')
        rol_buscado = request.args.get('rol')
        try:
            limit = int(request.args.get('_limit', 10))
            offset = int(request.args.get('_offset', 0))
        except ValueError:
            limit, offset = 10, 0

        try:
           if id_buscado:
                url_api = f'http://localhost:5000/api/usuarios/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_usuarios = [response.json()]
           elif email_buscado:
               url_api = f'http://localhost:5000/api/usuarios/email'
               response = requests.get(url_api, params={'email': email_buscado}, timeout=5)
               response.raise_for_status()
               lista_usuarios = [response.json().get('usuario')]
           elif rol_buscado:
               url_api = f'http://localhost:5000/api/usuarios/rol'
               params = {'rol': rol_buscado, '_limit': limit, '_offset': offset}
               response = requests.get(url_api, params=params, timeout=5)
               response.raise_for_status()
               lista_usuarios = response.json().get('data', [])
           else:
               params = {'limit': limit, 'offset': offset}
               url_api = f'http://localhost:5000/api/usuarios'
               response = requests.get(url_api, params=params, timeout=5)
               response.raise_for_status()
               lista_usuarios = response.json().get('data', [])
           print(f"{lista_usuarios}")
           return render_template('dashboard-usuarios.html', usuarios=lista_usuarios, limit=limit, offset=offset)

        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados.")
            return redirect(url_for('dashboard_usuarios'))
        except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500

@app.route('/dashboard/usuarios/crear', methods=['POST'])
def crear_usuario():
    datos = {
        "nombre_usuario": request.form.get('nombre_usuario'),
        "contrasena": request.form.get('contrasena'),
        "email": request.form.get('email'),
        "nombre": request.form.get('nombre'),
        "apellido": request.form.get('apellido'),
        "rol": request.form.get('rol')
    }
    try:
        url_api = f'http://localhost:5000/api/usuarios'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        print(f"DEBUG: Enviando datos: {datos}") # <--- Mira esto en tu terminal
        flash("Usuario creado con éxito")
    except requests.exceptions.HTTPError as e:
        flash(f"Error: {e.response.text}")
    except requests.exceptions.RequestException as e:
        flash("Error al crear el usuario")
    return redirect(url_for('dashboard_usuarios'))

@app.route('/dashboard/usuarios/editar/parcial', methods=['POST'])
def editar_usuario_parcial():
    id_usuario = request.form.get('id_usuario')
    datos = {
        "email": request.form.get('email'),
        "contrasena": request.form.get('password')
    }
    datos = {k: v for k, v in datos.items() if v}
    try:
        url_api = f'http://localhost:5000/api/usuarios/{id_usuario}'
        response = requests.patch(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Email y contraseña actualizados con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el email y la contraseña del usuario")

    return redirect(url_for('dashboard_usuarios'))

@app.route('/dashboard/usuarios/editar/completo', methods=['POST'])
def editar_usuario_completo():
    id_usuario = request.form.get('id_usuario')
    datos_completos = {
        "nombre_usuario": request.form.get('usuario'),
        "contrasena": request.form.get('password'),
        "email": request.form.get('email'),
        "nombre": request.form.get('nombre'),
        "apellido": request.form.get('apellido'),
        "rol": request.form.get('rol')
    }
    
    datos_completos = {k: v for k, v in datos_completos.items() if v}
    try:
        url_api = f'http://localhost:5000/api/usuarios/{id_usuario}'
        response = requests.put(url_api,  json=datos_completos, timeout=5)
        response.raise_for_status()
        flash("Usuario actualizado con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el usuario")

    return redirect(url_for('dashboard_usuarios'))

@app.route('/dashboard/usuarios/credenciales', methods=['POST'])
def obtener_credenciales():
    email = request.form.get('email')
    try:
        url_api = 'http://localhost:5000/api/usuarios/credenciales'
        response = requests.post(url_api, json={'email': email}, timeout=5)
        response.raise_for_status()
        credenciales = response.json()
        flash(f"Credenciales encontradas: {credenciales}")
    except requests.exceptions.RequestException:
        flash("Error al obtener las credenciales")
    return redirect(url_for('dashboard_usuarios'))
  

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-not-found.html'),404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
