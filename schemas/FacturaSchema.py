from marshmallow import Schema, fields

class FacturaSchema(Schema):
    id_factura = fields.Int(dump_only=True)
    numeroFactura = fields.Int(required=True)  
    valor = fields.Float(required=True)
    fecha = fields.Date(dump_only=True) 
    id_reporteMensual = fields.Int(required = True) 