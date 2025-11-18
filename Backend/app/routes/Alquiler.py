from flask import Blueprint, jsonify, request
from app.services.AlquilerService import (
    obtener_todos_alquileres_service,
    obtener_alquiler_por_id_service,
    crear_alquiler_service,
    actualizar_alquiler_service,
    eliminar_alquiler_service
)

alquileres_bp = Blueprint("alquileres_bp", __name__, url_prefix="/alquileres")

@alquileres_bp.route("/", methods=["GET"])
def get_alquileres():
    try:
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
