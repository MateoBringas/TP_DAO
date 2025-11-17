from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Importar y registrar los blueprints
    from app.routes.Vehiculo import vehiculos_bp
    from app.routes.Cliente import clientes_bp
    from app.routes.Alquiler import alquileres_bp
    from app.routes.Reserva import reservas_bp
    from app.routes.Mantenimiento import mantenimientos_bp
    from app.routes.Reporte import reportes_bp

    app.register_blueprint(vehiculos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(alquileres_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(mantenimientos_bp)
    app.register_blueprint(reportes_bp)

    return app
