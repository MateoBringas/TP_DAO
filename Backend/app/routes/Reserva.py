from flask import Blueprint, jsonify, request
from app.services.ReservaService import (
    obtener_todas_reservas_service,
    obtener_reservas_con_filtros_service,
    obtener_reserva_por_id_service,
    crear_reserva_service,
    actualizar_reserva_service,
    eliminar_reserva_service
)

reservas_bp = Blueprint("reservas_bp", __name__, url_prefix="/reservas")

@reservas_bp.route("/", methods=["GET"])
def get_reservas():
    """
    Obtiene reservas con filtros opcionales.

    Query Parameters:
        estado_id (int): ID del estado de reserva
        fecha_desde (str): Fecha de inicio del rango (YYYY-MM-DD)
        fecha_hasta (str): Fecha de fin del rango (YYYY-MM-DD)

    Examples:
        GET /reservas/
        GET /reservas/?estado_id=1
        GET /reservas/?fecha_desde=2025-01-01&fecha_hasta=2025-12-31
        GET /reservas/?estado_id=2&fecha_desde=2025-01-01&fecha_hasta=2025-12-31
    """
    try:
        estado_id = request.args.get('estado_id', type=int)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)

        # Si hay filtros, usar la función con filtros
        if estado_id is not None or fecha_desde is not None or fecha_hasta is not None:
            reservas = obtener_reservas_con_filtros_service(
                estado_id=estado_id,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta
            )
        else:
            # Si no hay filtros, obtener todas
            reservas = obtener_todas_reservas_service()

        return jsonify(reservas), 200
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
