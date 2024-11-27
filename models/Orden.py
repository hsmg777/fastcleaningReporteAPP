from db import db
from datetime import datetime


class Orden(db.Model):  
    __tablename__ = 'Orden'  
    id_orden = db.Column(db.Integer, primary_key=True)  
    numeroOrden = db.Column(db.Integer, nullable=False)  
    valor = db.Column(db.Float, nullable=False) 
    fecha = db.Column(db.Date, default=datetime.utcnow)  
    id_reporteMensual = db.Column(db.Integer, nullable=True)

    def __init__(self, numeroOrden, valor, fecha, id_reporteMensual):
        self.numeroOrden = numeroOrden
        self.valor = valor
        self.fecha = fecha or datetime.utcnow().date()
        self.id_reporteMensual = id_reporteMensual

    