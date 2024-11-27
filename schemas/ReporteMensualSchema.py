from marshmallow import Schema, fields

class ReporteMensualSchema(Schema):
    id_reporteMensual = fields.Int(dump_only=True)  # Campo solo para salida
    nombreMes = fields.Str(required=True, validate=lambda x: len(x) <= 50)  # Validar longitud
    totalNeto = fields.Float(dump_only=True)  # Calculado automáticamente
    totalGastos = fields.Float(dump_only=True)  # Calculado automáticamente
    ganancia = fields.Float(dump_only=True)  # Calculado automáticamente
