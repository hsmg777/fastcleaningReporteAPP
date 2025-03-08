from marshmallow import Schema, fields

class FacturaSchema(Schema):
    id_factura = fields.Int(dump_only=True)
    numeroFactura = fields.Int(required=True)  
    valor = fields.Float(required=True)
    fecha = fields.Date(required=False)  # Hacer opcional
    id_reporteMensual = fields.Int(required=False)  # Permitir que sea `None`
