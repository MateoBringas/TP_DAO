from flask import Blueprint, jsonify, request
from app.services.MantenimientoService import (
    obtener_todos_mantenimientos_service,
    obtener_mantenimiento_por_id_service,
    crear_mantenimiento_service,
    actualizar_mantenimiento_service,
    eliminar_mantenimiento_service
)

mantenimientos_bp = Blueprint("mantenimientos_bp", __name__, url_prefix="/mantenimientos")

@mantenimientos_bp.route("/", methods=["GET"])
def get_mantenimientos():
    try:
        mantenimientos = obtener_todos_mantenimientos_service()
        return jsonify([m.to_dict() for m in mantenimientos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mantenimientos_bp.route("/<int:id_mantenimiento>", methods=["GET"])
def get_mantenimiento(id_mantenimiento):
    try:
        mantenimiento = obtener_mantenimiento_por_id_service(id_mantenimiento)
        if mantenimiento:
            return jsonify(mantenimiento.to_dict()), 200
        return jsonify({"error": "Mantenimiento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mantenimientos_bp.route("/", methods=["POST"])
def post_mantenimiento():
    try:
        data = request.get_json()
        nuevo_mantenimiento = crear_mantenimiento_service(data)
        return jsonify(nuevo_mantenimiento.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mantenimientos_bp.route("/<int:id_mantenimiento>", methods=["PUT"])
def put_mantenimiento(id_mantenimiento):
    try:
        data = request.get_json()
        mantenimiento_actualizado = actualizar_mantenimiento_service(id_mantenimiento, data)
        return jsonify(mantenimiento_actualizado.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@mantenimientos_bp.route("/<int:id_mantenimiento>", methods=["DELETE"])
def delete_mantenimiento(id_mantenimiento):
    try:
        eliminado = eliminar_mantenimiento_service(id_mantenimiento)
        if eliminado:
            return jsonify({"message": "Mantenimiento eliminado correctamente"}), 200
        return jsonify({"error": "Mantenimiento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
