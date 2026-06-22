import os
import sys
import requests
from functools import wraps
from api.app import app as api_app
from flask import Blueprint, request, jsonify, url_for, flash, redirect, render_template
from api.utils.pagination import build_links

landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    try:
        resp = requests.get('http://localhost:5000/api/servicios/estado/habilitado')
        data = resp.json()
        servicios = data if isinstance(data, list) else data.get('data', [])
        print(f"Servicios cargados: {servicios}")
    except:
        servicios = []
        print("Sin servicios")
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fecha_raw = request.form.get('fecha')
        horario_raw = request.form.get('horario')
        fecha_datetime = f"{fecha_raw} {horario_raw}:00" if fecha_raw and horario_raw else None

        comensales_form = request.form.get('comensales') or '0'

        data = {
            "cantidad_personas": int(comensales_form),
            "fecha": fecha_datetime,
            "nombre": nombre,
            "apellido": apellido,
            "email": request.form.get('email'),
            "DNI": request.form.get('documento'),
            "telefono": request.form.get('telefono'),
            "comentario": request.form.get('comentario') or None,
        }

        try:
            response = requests.post('http://localhost:5000/api/reservas', json=data)

            if response.status_code == 201:
                reserva_id = response.json().get('reserva_id')
                serv_seleccionados = request.form.getlist('servicios')

                if serv_seleccionados and reserva_id:
                    requests.put(f'http://localhost:5000/api/servicios-reservas/{reserva_id}', json ={"servicios_id": [int(s) for s in serv_seleccionados]})
                
                flash('Se realizó la reserva con exito.', 'success')
                return redirect(url_for('landing.reservas'))
            elif response.status_code == 409:
                flash("No hay disponibilidad de mesas.", "error")
                return redirect(url_for('landing.reservas'))
            else:
                error_msg = response.json().get('errors', [{}])[0].get('message', 'Ha ocurrido un error inesperado')
                flash(error_msg, 'error')
        
        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            flash('Error de conexión.', 'error')


    return render_template('reservas.html', servicios=servicios)

@landing_bp.route('/cancelar', methods=['GET', 'POST'])
def pagina_cancelada():
    if request.method == 'POST':
        id_reserva = request.form.get('id')
        dni_ingresado= request.form.get('dni', '').strip()
        
        if not id_reserva or not dni_ingresado:
            flash("Debes completar el DNI para continuar.")
            return render_template('cancelar.html', reserva_id=id_reserva)
        
        try:
            resp = requests.get(f'http://localhost:5000/api/reservas/{id_reserva}', timeout=5)
            if resp.status_code == 404:
                flash("No se encontró la reserva")
                return render_template('cancelar.html')
            
            resp.raise_for_status()
            reserva = resp.json()

            if reserva.get('estado') in ('finalizada', 'cancelada'):
                flash(f"Esta reserva ya está {reserva['estado']}")
                return render_template('cancelar.html')
            if str(reserva.get('DNI')) != dni_ingresado:
                flash("El DNI ingresado no coincide con el de la reserva.")
                return render_template('cancelar.html', reserva_id=id_reserva)

            url_api = f'http://localhost:5000/api/reservas/{id_reserva}/cancelar'
            response = requests.patch(url_api, timeout=5)
            response.raise_for_status()

            flash("Reserva cancelada con éxito")
            return render_template('cancelar.html', cancelada=True)

        except requests.exceptions.RequestException as e:
            flash(f"Error en la operación: {e}")
            return render_template('cancelar.html', reserva_id=id_reserva)

    id_reserva = request.args.get('id')
    if not id_reserva:
        flash("El enlace no es válido")
        return render_template('cancelar.html')

    try:
        resp = requests.get(f'http://localhost:5000/api/reservas/{id_reserva}', timeout=5)
        if resp.status_code == 404:
            flash("No se encontró la reserva")
            return render_template('cancelar.html')
        
        resp.raise_for_status()
        reserva = resp.json()

        if reserva.get('estado') in ('finalizada', 'cancelada'):
            flash(f"Esta reserva ya está {reserva['estado']}")
            return render_template('cancelar.html')
            
    except requests.exceptions.RequestException as e:
        flash(f"Error en la operación: {e}", "error")
        return render_template('cancelar.html')

    return render_template('cancelar.html', reserva_id=id_reserva)

@landing_bp.route('/datos-reserva/<int:id>', methods=['GET']) 
def datos_reserva(id):
    try:
        datos = requests.get(f"http://localhost:5000/api/reservas/{id}")
        servicios = requests.get(f"http://localhost:5000/api/servicios-reservas/{id}")

        if datos.status_code != 200:
            return redirect(url_for('landing.inicio'))
        
        reserva_data = datos.json()
        
        servicios_lista = []
        if servicios.status_code == 200:
            servicios_data = servicios.json()
            for item in servicios_data:
                id_servicio = item.get('servicio_id')
                
                resp_servicio = requests.get(f"http://localhost:5000/api/servicios/{id_servicio}")
                
                if resp_servicio.status_code == 200:
                    servicios_lista.append(resp_servicio.json())

        return render_template('datos-qr-reserva.html', reserva=reserva_data, servicios=servicios_lista)
    
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return redirect(url_for('landing.inicio'))

@landing_bp.route('/')
def index():
    return render_template('inicio.html')


@landing_bp.route('/menu', endpoint='menu')
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

@landing_bp.route('/resenas')
def resenas():       
    limit = request.args.get('limit', default=3, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    with api_app.test_client() as client:
        resenas_resp = client.get('/resenas', query_string={'_limit': limit, '_offset': offset, 'estado':'habilitada'})
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

@landing_bp.route('/calificar', methods=['GET', 'POST'])
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
            return redirect(url_for('landing.resena_enviada', reserva_id=reserva_id))
        
        if response.status_code == 409:
            flash('Ya existe una reseña para esta reserva.', 'error')
        elif response.status_code == 404:
            flash('No se encontró la reserva.', 'error')
        else:
            flash('Ha ocurrido un error', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('landing.calificar', reserva_id=reserva_id))

@landing_bp.route('/resena-enviada')
def resena_enviada():
    reserva_id = request.args.get('reserva_id', type=int)

    if reserva_id is None:
        return redirect(url_for('landing.index'))
    
    return render_template('resena-enviada.html', reserva_id=reserva_id)