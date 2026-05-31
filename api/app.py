from flask import Flask
from flask_cors import CORS
from api.routes.menu import menu_bp
from api.routes.categorias import categorias_bp
from api.routes.reserva import reservas_bp
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# registren los blueprints de cada módulo s
app.register_blueprint(menu_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(reservas_bp, url_prefix='/api')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
