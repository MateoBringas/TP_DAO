from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.services.VehiculoService import (
    obtener_todos_vehiculos_service,
    crear_vehiculo_service,
    obtener_vehiculos_disponibles_service,
    actualizar_vehiculo_service
)

vehiculos_bp = Blueprint("vehiculos_bp", __name__, url_prefix="/vehiculos")

# Configuración para subida de archivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


# PUT /vehiculos/<id>
@vehiculos_bp.route("/<int:id_vehiculo>", methods=["PUT"])
def put_vehiculo(id_vehiculo):
    try:
        data = request.get_json()
        vehiculo_actualizado = actualizar_vehiculo_service(id_vehiculo, data)
        return jsonify(vehiculo_actualizado.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST /vehiculos/upload-foto
@vehiculos_bp.route("/upload-foto", methods=["POST"])
def upload_foto():
    try:
        if 'foto' not in request.files:
            return jsonify({"error": "No se envió ningún archivo"}), 400

        file = request.files['foto']

        if file.filename == '':
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400

        if file and allowed_file(file.filename):
            # Generar nombre único para el archivo
            import uuid
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{extension}"

            # Asegurar que el directorio existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Guardar archivo
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Devolver la URL relativa
            foto_url = f"/static/uploads/{filename}"
            return jsonify({"foto_url": foto_url}), 200

        return jsonify({"error": "Tipo de archivo no permitido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /static/uploads/<filename>
@vehiculos_bp.route("/static/uploads/<filename>", methods=["GET"])
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
