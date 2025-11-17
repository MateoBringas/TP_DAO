from flask import Blueprint, jsonify, request
from app.services.VehiculoService import (
    obtener_todos_vehiculos_service,
    crear_vehiculo_service,
    obtener_vehiculos_disponibles_service
)

vehiculos_bp = Blueprint("vehiculos_bp", __name__, url_prefix="/vehiculos")

# GET /disponibles?fecha_inicio=...&fecha_prevista=...
@vehiculos_bp.route("/disponibles", methods=["GET"])
def get_vehiculos_disponibles():
    try:
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_prevista = request.args.get("fecha_prevista")

        if not fecha_inicio or not fecha_prevista:
            return jsonify({"error": "Se requieren fecha_inicio y fecha_prevista"}), 400

        vehiculos = obtener_vehiculos_disponibles_service(fecha_inicio, fecha_prevista)
        return jsonify([v.to_dict() for v in vehiculos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
