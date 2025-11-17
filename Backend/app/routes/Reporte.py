from flask import Blueprint, jsonify, request
from app.database.database import get_connection

reportes_bp = Blueprint("reportes_bp", __name__, url_prefix="/reportes")

@reportes_bp.route("/vehiculos-mas-alquilados", methods=["GET"])
def get_vehiculos_mas_alquilados():
    """Reporte de vehículos más alquilados"""
    try:
        query = """
            SELECT
                v.id_vehiculo,
                v.patente,
                v.marca,
                v.modelo,
                COUNT(a.id_alquiler) as cantidad_alquileres,
                SUM(JULIANDAY(COALESCE(a.fecha_entrega, a.fecha_prevista)) - JULIANDAY(a.fecha_inicio)) as dias_alquilados
            FROM vehiculos v
            LEFT JOIN alquileres a ON v.id_vehiculo = a.vehiculo_id
            GROUP BY v.id_vehiculo, v.patente, v.marca, v.modelo
            ORDER BY cantidad_alquileres DESC
            LIMIT 10
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()

            datos = []
            for fila in resultados:
                datos.append({
                    "id_vehiculo": fila["id_vehiculo"],
                    "patente": fila["patente"],
                    "marca": fila["marca"],
                    "modelo": fila["modelo"],
                    "cantidad_alquileres": fila["cantidad_alquileres"],
                    "dias_alquilados": round(fila["dias_alquilados"] if fila["dias_alquilados"] else 0, 2)
                })

            return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reportes_bp.route("/ingresos-mensuales", methods=["GET"])
def get_ingresos_mensuales():
    """Reporte de ingresos mensuales (calculado desde alquileres)"""
    try:
        anio = request.args.get("anio", "2024")

        query = """
            SELECT
                strftime('%m', a.fecha_entrega) as mes,
                strftime('%Y', a.fecha_entrega) as anio,
                SUM((JULIANDAY(a.fecha_entrega) - JULIANDAY(a.fecha_inicio)) * v.tarifa_base_dia) as total_ingresos,
                COUNT(a.id_alquiler) as cantidad_alquileres
            FROM alquileres a
            JOIN vehiculos v ON a.vehiculo_id = v.id_vehiculo
            WHERE a.fecha_entrega IS NOT NULL
              AND a.fecha_entrega < DATE('now')
              AND strftime('%Y', a.fecha_entrega) = ?
            GROUP BY mes, anio
            ORDER BY anio, mes
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (anio,))
            resultados = cursor.fetchall()

            meses = {
                "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
                "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
                "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
            }

            datos = []
            for fila in resultados:
                datos.append({
                    "mes": fila["mes"],
                    "mes_nombre": meses.get(fila["mes"], fila["mes"]),
                    "anio": fila["anio"],
                    "total_ingresos": float(fila["total_ingresos"]),
                    "cantidad_pagos": fila["cantidad_alquileres"]
                })

            return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reportes_bp.route("/clientes-top", methods=["GET"])
def get_clientes_top():
    """Reporte de mejores clientes"""
    try:
        query = """
            SELECT
                c.id_cliente,
                c.nombre,
                c.apellido,
                c.email,
                COUNT(a.id_alquiler) as cantidad_alquileres,
                SUM(JULIANDAY(COALESCE(a.fecha_entrega, a.fecha_prevista)) - JULIANDAY(a.fecha_inicio)) as dias_totales
            FROM clientes c
            LEFT JOIN alquileres a ON c.id_cliente = a.cliente_id
            GROUP BY c.id_cliente, c.nombre, c.apellido, c.email
            HAVING COUNT(a.id_alquiler) > 0
            ORDER BY cantidad_alquileres DESC
            LIMIT 10
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()

            datos = []
            for fila in resultados:
                datos.append({
                    "id_cliente": fila["id_cliente"],
                    "nombre": fila["nombre"],
                    "apellido": fila["apellido"],
                    "email": fila["email"],
                    "cantidad_alquileres": fila["cantidad_alquileres"],
                    "dias_totales": round(fila["dias_totales"] if fila["dias_totales"] else 0, 2)
                })

            return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reportes_bp.route("/mantenimientos-proximos", methods=["GET"])
def get_mantenimientos_proximos():
    """Reporte de mantenimientos próximos"""
    try:
        query = """
            SELECT
                m.id_mantenimiento,
                v.id_vehiculo,
                v.patente,
                v.marca,
                v.modelo,
                m.fecha_programada,
                m.km,
                m.estado_mantenimiento,
                v.km_actual
            FROM mantenimientos m
            JOIN vehiculos v ON m.vehiculo_id = v.id_vehiculo
            WHERE m.estado_mantenimiento IN ('PROGRAMADO', 'EN_CURSO')
            ORDER BY m.fecha_programada ASC
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()

            datos = []
            for fila in resultados:
                datos.append({
                    "id_mantenimiento": fila["id_mantenimiento"],
                    "id_vehiculo": fila["id_vehiculo"],
                    "patente": fila["patente"],
                    "marca": fila["marca"],
                    "modelo": fila["modelo"],
                    "fecha_programada": fila["fecha_programada"],
                    "km": fila["km"],
                    "estado_mantenimiento": fila["estado_mantenimiento"],
                    "km_actual": fila["km_actual"]
                })

            return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reportes_bp.route("/estadisticas-generales", methods=["GET"])
def get_estadisticas_generales():
    """Estadísticas generales del sistema"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Total de vehículos
            cursor.execute("SELECT COUNT(*) as total FROM vehiculos WHERE habilitado = 1")
            total_vehiculos = cursor.fetchone()["total"]

            # Total de clientes
            cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE habilitado = 1")
            total_clientes = cursor.fetchone()["total"]

            # Alquileres activos
            cursor.execute("""
                SELECT COUNT(*) as total FROM alquileres
                WHERE estado_alquiler_id IN (
                    SELECT id_estado_alquiler FROM estados_alquiler WHERE codigo IN ('ACTIVO', 'PENDIENTE')
                )
            """)
            alquileres_activos = cursor.fetchone()["total"]

            # Reservas pendientes
            cursor.execute("""
                SELECT COUNT(*) as total FROM reservas
                WHERE estado_reserva_id IN (
                    SELECT id_estado_reserva FROM estados_reserva WHERE codigo = 'PENDIENTE'
                )
            """)
            reservas_pendientes = cursor.fetchone()["total"]

            # Ingresos del mes actual (calculado desde alquileres)
            cursor.execute("""
                SELECT COALESCE(
                    SUM(
                        (JULIANDAY(a.fecha_entrega) - JULIANDAY(a.fecha_inicio)) * v.tarifa_base_dia
                    ), 0
                ) as total
                FROM alquileres a
                JOIN vehiculos v ON a.vehiculo_id = v.id_vehiculo
                WHERE a.fecha_entrega IS NOT NULL
                  AND a.fecha_entrega < DATE('now')
                  AND strftime('%Y-%m', a.fecha_entrega) = strftime('%Y-%m', 'now')
            """)
            ingresos_mes_actual = cursor.fetchone()["total"]

            datos = {
                "total_vehiculos": total_vehiculos,
                "total_clientes": total_clientes,
                "alquileres_activos": alquileres_activos,
                "reservas_pendientes": reservas_pendientes,
                "ingresos_mes_actual": float(ingresos_mes_actual)
            }

            return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
