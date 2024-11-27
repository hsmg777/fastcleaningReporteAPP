from marshmallow import Schema, fields

class GastosSchema(Schema):
    id_gastos = fields.Int(dump_only=True)  
    nombreGasto = fields.Str(required=True, validate=lambda x: len(x) <= 50)  
    valor = fields.Float(required=True)
    fecha = fields.Date(dump_only=True)  
    id_reporteMensual = fields.Int(required=True)
