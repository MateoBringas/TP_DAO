from flask import Blueprint, jsonify, request # type: ignore (Borrar despues, solo es estetico)
from app.services.VehiculoService import (
    obtener_todos_vehiculos_service,
    crear_vehiculo_service
)

vehiculos_bp = Blueprint("vehiculos_bp", __name__, url_prefix="/vehiculos")

# GET /
@vehiculos_bp.route("/", methods=["GET"])
def get_vehiculos():
    try:
        vehiculos = obtener_todos_vehiculos_service()
        return jsonify([v.to_dict() for v in vehiculos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /vehiculos
@vehiculos_bp.route("/", methods=["POST"])
def post_vehiculo():
    try:
        data = request.get_json()
        nuevo_vehiculo = crear_vehiculo_service(data)
        return jsonify(nuevo_vehiculo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
