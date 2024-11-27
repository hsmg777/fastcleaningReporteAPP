from db import db

class ReporteMensual(db.Model):
    __tablename__ = 'ReporteMensual'

    id_reporteMensual = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreMes = db.Column(db.String(50), nullable=False)
    totalNeto = db.Column(db.Float, default=0.0)
    totalGastos = db.Column(db.Float, default=0.0)
    ganancia = db.Column(db.Float, default=0.0)

    def __init__(self, nombreMes, totalNeto=0.0, totalGastos=0.0, ganancia=0.0):
        self.nombreMes = nombreMes
        self.totalNeto = totalNeto
        self.totalGastos = totalGastos
        self.ganancia = ganancia
