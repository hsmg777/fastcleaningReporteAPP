from marshmallow import Schema, fields

class OrdenSchema(Schema):
    id_orden = fields.Int(dump_only=True)
    numeroOrden = fields.Int(required=True)  
    valor = fields.Float(required=True)
    fecha = fields.Date(dump_only=True) 
    id_reporteMensual = fields.Int(required = True) 