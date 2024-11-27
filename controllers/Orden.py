from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models.Orden import Orden
from schemas.OrdenSchema import OrdenSchema
from sqlalchemy.sql import text  # Importar text para consultas SQL textuales

# Crear el Blueprint
blp = Blueprint("Orden", __name__, url_prefix="/tasks", description="Operaciones CRUD para Ordenes")

# Schemas
orden_schema = OrdenSchema()
ordenes_schema = OrdenSchema(many=True)


# Rutas para /tasks/ordenes
@blp.route('/ordenes')
class OrdenList(MethodView):
    @blp.response(200, OrdenSchema(many=True))  # Define el esquema para la respuesta
    def get(self):
        """Obtener todas las órdenes"""
        ordenes = Orden.query.all()
        return ordenes

    @blp.arguments(OrdenSchema)  # Valida la entrada con el esquema
    @blp.response(201, OrdenSchema)  # Define el esquema para la respuesta
    def post(self, data):
        """Crear una nueva orden"""
        try:
            # Crear la nueva orden
            nueva_orden = Orden(
                numeroOrden=data['numeroOrden'],
                valor=data['valor'],
                fecha=data.get('fecha'),
                id_reporteMensual=data['id_reporteMensual']
            )
            db.session.add(nueva_orden)
            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            stored_proc = text("EXEC sp_UpdateReporteMensual :id")
            db.session.execute(stored_proc, {'id': data['id_reporteMensual']})
            db.session.commit()

            return nueva_orden
        except Exception as e:
            abort(400, message=f"Error al crear la orden: {str(e)}")


# Rutas para /tasks/ordenes/<int:id_orden>
@blp.route('/ordenes/<int:id_orden>')
class OrdenResource(MethodView):
    @blp.response(200, OrdenSchema)  # Define el esquema para la respuesta
    def get(self, id_orden):
        """Obtener una orden por su ID"""
        orden = Orden.query.get_or_404(id_orden)
        return orden

    @blp.arguments(OrdenSchema)  # Valida la entrada con el esquema
    @blp.response(200, OrdenSchema)  # Define el esquema para la respuesta
    def put(self, data, id_orden):
        """Actualizar una orden existente"""
        try:
            orden = Orden.query.get_or_404(id_orden)
            if 'numeroOrden' in data:
                orden.numeroOrden = data['numeroOrden']
            if 'valor' in data:
                orden.valor = data['valor']
            if 'fecha' in data:
                orden.fecha = data['fecha']
            if 'id_reporteMensual' in data:
                orden.id_reporteMensual = data['id_reporteMensual']

            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            stored_proc = text("EXEC sp_UpdateReporteMensual :id")
            db.session.execute(stored_proc, {'id': orden.id_reporteMensual})
            db.session.commit()

            return orden
        except Exception as e:
            abort(400, message=f"Error al actualizar la orden: {str(e)}")

    @blp.response(204)  # Sin contenido en la respuesta
    def delete(self, id_orden):
        """Eliminar una orden"""
        try:
            orden = Orden.query.get_or_404(id_orden)
            id_reporteMensual = orden.id_reporteMensual  # Capturar el ID del reporte antes de eliminar
            db.session.delete(orden)
            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            stored_proc = text("EXEC sp_UpdateReporteMensual :id")
            db.session.execute(stored_proc, {'id': id_reporteMensual})
            db.session.commit()

            return '', 204
        except Exception as e:
            abort(400, message=f"Error al eliminar la orden: {str(e)}")
