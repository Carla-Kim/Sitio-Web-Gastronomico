from flask import Flask
from flask_cors import CORS

# importen los blueprints de cada módulo
    # from users.routes import users_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# registren los blueprints de cada módulo
    # app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)