import os
from flask import Flask
from flask_cors import CORS
from api.routes.menu import menu_bp
from api.routes.categorias import categorias_bp
from api.routes.reserva import reservas_bp
from api.routes.mesa import mesa_bp
from api.routes.resenas import resenas_bp
from api.routes.servicio import servicio_bp
from api.routes.servicios_reservas import servicio_reserva_bp
from api.routes.usuario import usuarios_bp
from api.routes.stats import stats_bp

base_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(base_dir)
templates_path = os.path.join(project_root, 'web', 'templates')

app = Flask(__name__, template_folder=templates_path)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(menu_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(resenas_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(mesa_bp)
app.register_blueprint(servicio_bp)
app.register_blueprint(servicio_reserva_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(stats_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
