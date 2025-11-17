from flask import Blueprint, jsonify, request
from app.services.ReservaService import (
    obtener_todas_reservas_service,
    obtener_reserva_por_id_service,
    crear_reserva_service,
    actualizar_reserva_service,
    eliminar_reserva_service
)

reservas_bp = Blueprint("reservas_bp", __name__, url_prefix="/reservas")

@reservas_bp.route("/", methods=["GET"])
def get_reservas():
    try:
        reservas = obtener_todas_reservas_service()
        return jsonify([r.to_dict() for r in reservas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservas_bp.route("/<int:id_reserva>", methods=["GET"])
def get_reserva(id_reserva):
    try:
        reserva = obtener_reserva_por_id_service(id_reserva)
        if reserva:
            return jsonify(reserva.to_dict()), 200
        return jsonify({"error": "Reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservas_bp.route("/", methods=["POST"])
def post_reserva():
    try:
        data = request.get_json()
        nueva_reserva = crear_reserva_service(data)
        return jsonify(nueva_reserva.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservas_bp.route("/<int:id_reserva>", methods=["PUT"])
def put_reserva(id_reserva):
    try:
        data = request.get_json()
        reserva_actualizada = actualizar_reserva_service(id_reserva, data)
        return jsonify(reserva_actualizada.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reservas_bp.route("/<int:id_reserva>", methods=["DELETE"])
def delete_reserva(id_reserva):
    try:
        eliminado = eliminar_reserva_service(id_reserva)
        if eliminado:
            return jsonify({"message": "Reserva eliminada correctamente"}), 200
        return jsonify({"error": "Reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
