from flask import Blueprint, jsonify, request
from app.services.ClienteService import (
    obtener_todos_clientes_service,
    obtener_cliente_por_id_service,
    crear_cliente_service,
    actualizar_cliente_service,
    eliminar_cliente_service
)

clientes_bp = Blueprint("clientes_bp", __name__, url_prefix="/clientes")

# GET /clientes/
@clientes_bp.route("/", methods=["GET"])
def get_clientes():
    try:
        clientes = obtener_todos_clientes_service()
        return jsonify([c.to_dict() for c in clientes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /clientes/<id>
@clientes_bp.route("/<int:id_cliente>", methods=["GET"])
def get_cliente(id_cliente):
    try:
        cliente = obtener_cliente_por_id_service(id_cliente)
        if cliente:
            return jsonify(cliente.to_dict()), 200
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /clientes/
@clientes_bp.route("/", methods=["POST"])
def post_cliente():
    try:
        data = request.get_json()
        nuevo_cliente = crear_cliente_service(data)
        return jsonify(nuevo_cliente.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /clientes/<id>
@clientes_bp.route("/<int:id_cliente>", methods=["PUT"])
def put_cliente(id_cliente):
    try:
        data = request.get_json()
        cliente_actualizado = actualizar_cliente_service(id_cliente, data)
        return jsonify(cliente_actualizado.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE /clientes/<id>
@clientes_bp.route("/<int:id_cliente>", methods=["DELETE"])
def delete_cliente(id_cliente):
    try:
        eliminado = eliminar_cliente_service(id_cliente)
        if eliminado:
            return jsonify({"message": "Cliente eliminado correctamente"}), 200
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
