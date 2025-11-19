from flask import Blueprint, jsonify, request
from app.services.AlquilerService import (
    obtener_todos_alquileres_service,
    obtener_alquileres_con_filtros_service,
    obtener_alquiler_por_id_service,
    crear_alquiler_service,
    actualizar_alquiler_service,
    eliminar_alquiler_service
)

alquileres_bp = Blueprint("alquileres_bp", __name__, url_prefix="/alquileres")

@alquileres_bp.route("/", methods=["GET"])
def get_alquileres():
    """
    Obtiene alquileres con filtros opcionales.

    Query Parameters:
        estado_id (int): ID del estado de alquiler
        fecha_desde (str): Fecha de inicio del rango (YYYY-MM-DD)
        fecha_hasta (str): Fecha de fin del rango (YYYY-MM-DD)

    Examples:
        GET /alquileres/
        GET /alquileres/?estado_id=1
        GET /alquileres/?fecha_desde=2025-01-01&fecha_hasta=2025-12-31
        GET /alquileres/?estado_id=2&fecha_desde=2025-01-01&fecha_hasta=2025-12-31
    """
    try:
        estado_id = request.args.get('estado_id', type=int)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)

        # Si hay filtros, usar la función con filtros
        if estado_id is not None or fecha_desde is not None or fecha_hasta is not None:
            alquileres = obtener_alquileres_con_filtros_service(
                estado_id=estado_id,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta
            )
        else:
            # Si no hay filtros, obtener todos
            alquileres = obtener_todos_alquileres_service()

        return jsonify(alquileres), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alquileres_bp.route("/<int:id_alquiler>", methods=["GET"])
def get_alquiler(id_alquiler):
    try:
        alquiler = obtener_alquiler_por_id_service(id_alquiler)
        if alquiler:
            return jsonify(alquiler.to_dict()), 200
        return jsonify({"error": "Alquiler no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alquileres_bp.route("/", methods=["POST"])
def post_alquiler():
    try:
        data = request.get_json()
        nuevo_alquiler = crear_alquiler_service(data)
        return jsonify(nuevo_alquiler.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alquileres_bp.route("/<int:id_alquiler>", methods=["PUT"])
def put_alquiler(id_alquiler):
    try:
        data = request.get_json()
        alquiler_actualizado = actualizar_alquiler_service(id_alquiler, data)
        return jsonify(alquiler_actualizado.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alquileres_bp.route("/<int:id_alquiler>", methods=["DELETE"])
def delete_alquiler(id_alquiler):
    try:
        eliminado = eliminar_alquiler_service(id_alquiler)
        if eliminado:
            return jsonify({"message": "Alquiler eliminado correctamente"}), 200
        return jsonify({"error": "Alquiler no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
