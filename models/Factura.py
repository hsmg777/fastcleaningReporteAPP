from db import db
from datetime import datetime


class Factura(db.Model):  
    __tablename__ = 'Factura'  
    id_factura = db.Column(db.Integer, primary_key=True)  
    numeroFactura = db.Column(db.Integer, nullable=False)  
    valor = db.Column(db.Float, nullable=False) 
    fecha = db.Column(db.Date, default=datetime.utcnow)  
    id_reporteMensual = db.Column(db.Integer, nullable=True)

    def __init__(self, numeroFactura, valor, fecha, id_reporteMensual):
        self.numeroFactura = numeroFactura
        self.valor = valor
        self.fecha = fecha or datetime.utcnow().date()
        self.id_reporteMensual = id_reporteMensual

    