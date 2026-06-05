import os
import requests
from functools import wraps
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    g
)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
API_URL = os.getenv("API_URL", "http://localhost:5000/api")
SECRET_KEY = os.getenv("SECRET_KEY", "basheros123")


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = SECRET_KEY


def login_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if usuario_actual() is None:
            return redirect('/dashboard/login')

        return view(*args, **kwargs)

    return wrapper

def admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        usuario = usuario_actual()

        if usuario is None:
            return redirect('/dashboard/login')

        if usuario["rol"] != "admin":
            return redirect('/dashboard')

        return view(*args, **kwargs)

    return wrapper


def usuario_actual():
    if hasattr(g, "usuario"):
        return g.usuario

    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        return None
    
    respuesta = requests.get(
        f'{API_URL}/usuarios/{usuario_id}'
    )

    if respuesta.status_code != 200:
        return None

    g.usuario = respuesta.json()
    return g.usuario


@app.route('/')
def index():
    return render_template('inicio.html')


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
# @login_requerido
def dashboard_reservas():  
    if request.method == 'POST':
       tipo = request.form.get('tipo')
       id_reserva = request.form.get('id_reserva')
       if not id_reserva:
           flash("No se pudo completar la acción: ID inexistente")
           return redirect(url_for('dashboard_reservas'))
       try:
            if tipo == 'reserva':
                url_api = f'http://localhost:5001/reservas/{id_reserva}/cancelar'
                response = requests.patch(url_api, timeout=5)
                response.raise_for_status()
                flash("Reserva cancelada con éxito")
            elif tipo == 'servicio-res':
                servicios_ids = request.form.getlist('servicios_seleccionados')
                try:
                    url_api = f'http://localhost:5001/servicios-reservas/{id_reserva}'
                    response = requests.put(url_api, json={"servicios_id": [int(i) for i in servicios_ids]}, timeout=5)
                    response.raise_for_status()
                    flash("Servicios asociados con éxito")
                except Exception as e:
                    flash("Error al asociar servicios")
            elif tipo == 'eliminar_servicio':
                try:
                    url_api = f'http://localhost:5001/servicios-reservas/{id_reserva}'
                    response = requests.delete(url_api, timeout=5)
                    response.raise_for_status()
                    flash("Servicios de la reserva eliminados con éxito")
                except Exception as e:
                    flash("Error al eliminar los servicios de la reserva")
            return redirect(url_for('dashboard_reservas'))
       except requests.exceptions.RequestException as e:
            print(f"Error al cancelar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
        estado = request.args.get('estado')
        fecha = request.args.get('fecha')
        id_buscado = request.args.get('id')

        try:
            limit = int(request.args.get('_limit', 10))
            offset = int(request.args.get('_offset', 0))
        except ValueError:
            limit, offset = 10, 0

        try:
            if id_buscado:
                url_api = f'http://localhost:5001/reservas/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_reservas = [response.json()]
            elif estado:
               url_api = f'http://localhost:5001/reservas/estado/{estado}'
               response = requests.get(url_api, params={'_limit': limit, '_offset': offset}, timeout=5)
               response.raise_for_status()
               lista_reservas = response.json().get('data', [])
            elif fecha:
               url_api = f'http://localhost:5001/reservas/fecha/{fecha}'
               response = requests.get(url_api, params={'_limit': limit, '_offset': offset}, timeout=5)
               response.raise_for_status()
               lista_reservas = response.json().get('data', [])
            else:
               url_api = 'http://localhost:5001/reservas'
               response = requests.get(url_api, params={'_limit': limit, '_offset': offset}, timeout=5)
               response.raise_for_status()
               lista_reservas = response.json().get('data', [])
            lista_servicios_reserva = []
            url_api_serv = f'http://localhost:5001/servicios-reservas'
            response_servicios = requests.get(url_api_serv, timeout=5)
            response_servicios.raise_for_status()
            lista_servicios = response_servicios.json().get('data', [])
            try:
                if id_buscado:
                    url_api_serv_relacion = f'http://localhost:5001/servicios-reservas/{id_buscado}'
                    response_relacion = requests.get(url_api_serv_relacion, timeout=5)
                    lista_servicios_reserva = response_relacion.json() if response_relacion.status_code == 200 else []
            except:
                lista_servicios_reserva = []
            return render_template('dashboard-reservas.html', reservas=lista_reservas, limit=limit, offset=offset, servicios = lista_servicios, servicios_reserva = lista_servicios_reserva)

        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los criterios seleccionados.")
            return redirect(url_for('dashboard_reservas'))
        except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500

@app.route('/dashboard/servicios/crear', methods=['POST'])
def crear_servicio():
    datos = {
        "nombre": request.form.get('nombre')
    }
    try:
        url_api = f'http://localhost:5001/servicios'
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
    id_servicio = request.form.get('id_servicio')
    nuevo_nombre = request.form.get('nombre')

    if not id_servicio or not nuevo_nombre:
        flash("Datos incompletos para la edición.")
        return redirect(url_for('dashboard_reservas'))
    
    try:
        url_api = f'http://localhost:5001/servicios/{id_servicio}'
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
    id_servicio = request.form.get('id_servicio')
    try:
        url_api = f'http://localhost:5001/servicios/{id_servicio}'
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
            url_api = f'http://localhost:5001/resenas/{resena_a_eliminar}'
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
            limit = int(request.args.get('_limit', 10))  
            offset = int(request.args.get('_offset', 0))  
       except ValueError:
            limit, offset = 10, 0

       try:
           if id_buscado:
                url_api = f'http://localhost:5001/resenas/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]

           elif id_reserva_buscada:
                url_api = f'http://localhost:5001/resenas/reserva/{id_reserva_buscada}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]

           else:
                params = {'limit': limit, 'offset': offset}
                url_api = f'http://localhost:5001/resenas'
                response = requests.get(url_api, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                lista_resenas = data.get('resenas', [])

           return render_template('dashboard-resenas.html', resenas=lista_resenas, limit=int(limit), offset=int(offset))
       
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
                url_api = f'http://localhost:5001/productos/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Producto eliminado con éxito")

               

            else:
                url_api = f'http://localhost:5001/categorias/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Categoria eliminada con éxito")

               

       except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
       return redirect(url_for('dashboard_menu'))
    else:
       try:
           limit = int(request.args.get('limit', 10))
           offset = int(request.args.get('offset', 0))
       except ValueError:
           limit, offset = 10, 0
           
       params_categorias = {'_limit': limit, '_offset': offset}
       params_productos = {'limit': limit, 'offset': offset}
       try:
           url_api_categorias = f'http://localhost:5001/categorias'
           url_api_productos = f'http://localhost:5001/productos'
           response_categorias = requests.get(url_api_categorias, params=params_categorias, timeout=5)
           response_categorias.raise_for_status()
           response_productos = requests.get(url_api_productos, params=params_productos, timeout=5)
           response_productos.raise_for_status()

           lista_categorias = response_categorias.json().get('data', [])
           lista_productos = response_productos.json().get('productos', [])
           return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias, params_categ=params_categorias, params_prod=params_productos)
       except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500
       
@app.route('/dashboard/menu/crear', methods=['POST'])
def crear_producto():
    try:
        precio = float(request.form.get('precio', 0))
        categoria_id = int(request.form.get('categoria_id', 0))
    except (ValueError, TypeError):
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu'))
    datos = {
        "nombre": request.form.get('nombre'),
        "descripcion": request.form.get('descripcion'),
        "precio": precio,
        "categorias_id": categoria_id
    }
    try:
        url_api = f'http://localhost:5001/productos'
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
        categoria_id = int(request.form.get('categoria_id', 0))
    except (ValueError, TypeError):
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu'))
    datos = {
        "categorias_id": categoria_id,
        "nombre": request.form.get('nombre'),
        "precio": precio,
        "descripcion": request.form.get('descripcion')
    }

    try:
        url_api = f'http://localhost:5001/productos/{id_producto}'
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
        url_api = f'http://localhost:5001/categorias'
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
        url_api = f'http://localhost:5001/categorias/{id_categoria}'
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
            url_api = f'http://localhost:5001/usuarios/{usuario_a_eliminar}'
            response = requests.delete(url_api, timeout=5)
            response.raise_for_status()
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
                url_api = f'http://localhost:5001/usuarios/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_usuarios = [response.json()]
           elif email_buscado:
               url_api = f'http://localhost:5001/usuarios/{email_buscado}'
               response = requests.get(url_api, timeout=5)
               response.raise_for_status()
               lista_usuarios = [response.json()]
           else:
               params = {'limit': limit, 'offset': offset}
               if rol_buscado:
                   params['rol'] = rol_buscado
               url_api = f'http://localhost:5001/usuarios'
               response = requests.get(url_api, params=params, timeout=5)
               response.raise_for_status()
               lista_usuarios = response.json()
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
        "nombre_usuario": request.form.get('usuario'),
        "contrasena": request.form.get('password'),
        "email": request.form.get('email'),
        "nombre": request.form.get('nombre'),
        "apellido": request.form.get('apellido'),
        "rol": request.form.get('rol')
    }
    try:
        url_api = f'http://localhost:5001/usuarios'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Usuario creado con éxito")
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
        url_api = f'http://localhost:5001/usuarios/{id_usuario}'
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
    try:
        url_api = f'http://localhost:5001/usuarios/{id_usuario}'
        response = requests.put(url_api,  json=datos_completos, timeout=5)
        response.raise_for_status()
        flash("Usuario actualizado con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el usuario")

    return redirect(url_for('dashboard_usuarios'))
  

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-not-found.html'),404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
