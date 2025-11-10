from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Importar y registrar los blueprints
    from app.routes.Vehiculo import vehiculos_bp
    app.register_blueprint(vehiculos_bp)

    return app
