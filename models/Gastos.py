from db import db
from datetime import datetime

class Gastos(db.Model):
    __tablename__ = 'Gastos'

    id_gastos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreGasto = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow().date)
    id_reporteMensual = db.Column(db.Integer, nullable=True)

  

    def __init__(self, nombreGasto, valor, fecha=None, id_reporteMensual=None):
        self.nombreGasto = nombreGasto
        self.valor = valor
        self.fecha = fecha or datetime.utcnow().date()
        self.id_reporteMensual = id_reporteMensual
