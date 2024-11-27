from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models.Gastos import Gastos
from schemas.GastosSchema import GastosSchema
from marshmallow import ValidationError

# Crear el Blueprint
blp = Blueprint("Gastos", __name__, url_prefix="/tasks/gastos", description="Operaciones CRUD para Gastos")

# Schemas
gastos_schema = GastosSchema()
gastos_list_schema = GastosSchema(many=True)


# Rutas para /tasks/gastos
@blp.route('/')
class GastosList(MethodView):
    @blp.response(200, GastosSchema(many=True))  # Define el esquema para la respuesta
    def get(self):
        """Obtener todos los gastos"""
        gastos = Gastos.query.all()
        return gastos

    @blp.arguments(GastosSchema)  # Valida la entrada con el esquema
    @blp.response(201, GastosSchema)  # Define el esquema para la respuesta
    def post(self, data):
        """Crear un nuevo gasto"""
        try:
            nuevo_gasto = Gastos(
                nombreGasto=data['nombreGasto'],
                valor=data['valor'],
                fecha=data.get('fecha'),  # Aceptar fecha si viene en el JSON
                id_reporteMensual = data['id_reporteMensual']
            )
            db.session.add(nuevo_gasto)
            db.session.commit()
            return nuevo_gasto
        except Exception as e:
            abort(400, message=f"Error al crear el gasto: {str(e)}")


# Rutas para /tasks/gastos/<int:id_gastos>
@blp.route('/<int:id_gastos>')
class GastosResource(MethodView):
    @blp.response(200, GastosSchema)  # Define el esquema para la respuesta
    def get(self, id_gastos):
        """Obtener un gasto por su ID"""
        gasto = Gastos.query.get_or_404(id_gastos)
        return gasto

    @blp.arguments(GastosSchema)  # Valida la entrada con el esquema
    @blp.response(200, GastosSchema)  # Define el esquema para la respuesta
    def put(self, data, id_gastos):
        """Actualizar un gasto existente"""
        gasto = Gastos.query.get_or_404(id_gastos)
        if 'nombreGasto' in data:
            gasto.nombreGasto = data['nombreGasto']
        if 'valor' in data:
            gasto.valor = data['valor']
        if 'fecha' in data:
            gasto.fecha = data['fecha']
        if 'id_reporteMensual' in data:
            gasto.id_reporteMensual = data['id_reporteMensual']
        db.session.commit()
        return gasto

    @blp.response(204)  # Sin contenido en la respuesta
    def delete(self, id_gastos):
        """Eliminar un gasto"""
        gasto = Gastos.query.get_or_404(id_gastos)
        db.session.delete(gasto)
        db.session.commit()
        return '', 204
