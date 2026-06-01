import os
from flask import Flask, render_template

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

@app.route('/')
def index():
    return render_template('inicio.html')
    

@app.route('/login')
def login():
    # hay que agregar lógica para manejar el inicio de sesión, validación de usuarios, etc. antes de mostrar esta página
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    # hay que agregar lógica para verificar si el usuario es admin o un usuario válido antes de mostrar esta página
    return render_template('admin.html')

@app.route('/resenas')
def resenas():
    return render_template('resenas.html')

@app.route('/reservas')
def reservas():
    return render_template('reservas.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)