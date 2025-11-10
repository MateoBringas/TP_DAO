

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id_vehiculo = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer)
    tarifa_base_dia = db.Column(db.Float)
    habilitado = db.Column(db.Boolean, default=True)