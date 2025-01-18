from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models.Factura import Factura
from schemas.FacturaSchema import FacturaSchema
from sqlalchemy.sql import text

# Crear el Blueprint
blp = Blueprint("Factura", __name__, url_prefix="/tasks", description="Operaciones CRUD para Factura")

# Schemas
factura_schema = FacturaSchema()  # Para un único objeto
facturas_schema = FacturaSchema(many=True)  # Para listas de objetos


# Rutas para /tasks/facturas
@blp.route('/facturas')
class FacturasList(MethodView):
    @blp.response(200, FacturaSchema(many=True))  # Define el esquema para la respuesta
    def get(self):
        """Obtener todas las facturas"""
        facturas = Factura.query.all()
        return facturas

    @blp.arguments(FacturaSchema)  # Valida la entrada con el esquema
    @blp.response(201, FacturaSchema)  # Define el esquema para la respuesta
    def post(self, data):
        """Crear una nueva factura"""
        try:
            # Validar si el número de factura ya existe
            factura_existente = Factura.query.filter_by(numeroFactura=data['numeroFactura']).first()
            if factura_existente:
                abort(400, message="El número de factura ya existe.")

            # Crear la nueva factura
            nueva_factura = Factura(
                numeroFactura=data['numeroFactura'],
                valor=data['valor'],
                fecha=data.get('fecha'),  # Usará la fecha proporcionada o el valor predeterminado del modelo
                id_reporteMensual=data.get('id_reporteMensual')
            )
            db.session.add(nueva_factura)
            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            if nueva_factura.id_reporteMensual:
                stored_proc = text("EXEC sp_UpdateReporteMensual :id")
                db.session.execute(stored_proc, {'id': nueva_factura.id_reporteMensual})
                db.session.commit()

            return nueva_factura
        except Exception as e:
            abort(400, message=f"Error al crear la factura: {str(e)}")


# Nuevo endpoint para obtener facturas por id_reporteMensual
@blp.route('/factura/reporte/<int:id_reporteMensual>')
class FacturaByReporte(MethodView):
    @blp.response(200, FacturaSchema(many=True))
    def get(self, id_reporteMensual):
        """Obtener facturas por ID de reporte mensual"""
        try:
            # Validar que el reporte mensual exista
            reporte = db.session.execute(
                text("SELECT id_reporteMensual FROM ReporteMensual WHERE id_reporteMensual = :id"),
                {'id': id_reporteMensual}
            ).fetchone()
            if not reporte:
                abort(404, message="El reporte mensual no existe.")

            # Consulta SQL para las facturas
            query = text("SELECT * FROM Factura WHERE id_reporteMensual = :id_reporteMensual ORDER BY numeroFactura ASC")
            result = db.session.execute(query, {'id_reporteMensual': id_reporteMensual}).fetchall()
            return [dict(row) for row in result]
        except Exception as e:
            abort(400, message=f"Error al obtener las facturas: {str(e)}")


# Rutas para /tasks/facturas/<int:id_factura>
@blp.route('/factura/<int:id_factura>')
class FacturasResource(MethodView):
    @blp.response(200, FacturaSchema)  # Define el esquema para la respuesta
    def get(self, id_factura):
        """Obtener una factura por su ID"""
        factura = Factura.query.get_or_404(id_factura)
        return factura

    @blp.arguments(FacturaSchema)  # Valida la entrada con el esquema
    @blp.response(200, FacturaSchema)  # Define el esquema para la respuesta
    def put(self, data, id_factura):
        """Actualizar una factura existente"""
        try:
            factura = Factura.query.get_or_404(id_factura)

            # Validar si el número de factura ya existe en otra factura
            factura_existente = Factura.query.filter(Factura.numeroFactura == data['numeroFactura'], Factura.id != id_factura).first()
            if factura_existente:
                abort(400, message="El número de factura ya existe en otra factura.")

            if 'numeroFactura' in data:
                factura.numeroFactura = data['numeroFactura']
            if 'valor' in data:
                factura.valor = data['valor']
            if 'fecha' in data:
                factura.fecha = data['fecha']
            if 'id_reporteMensual' in data:
                # Validar si el nuevo id_reporteMensual existe
                reporte = db.session.execute(
                    text("SELECT id_reporteMensual FROM ReporteMensual WHERE id_reporteMensual = :id"),
                    {'id': data['id_reporteMensual']}
                ).fetchone()
                if not reporte:
                    abort(404, message="El reporte mensual no existe.")
                factura.id_reporteMensual = data['id_reporteMensual']

            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            if factura.id_reporteMensual:
                stored_proc = text("EXEC sp_UpdateReporteMensual :id")
                db.session.execute(stored_proc, {'id': factura.id_reporteMensual})
                db.session.commit()

            return factura
        except Exception as e:
            abort(400, message=f"Error al actualizar la factura: {str(e)}")

    @blp.response(204)  # Sin contenido en la respuesta
    def delete(self, id_factura):
        """Eliminar una factura"""
        try:
            factura = Factura.query.get_or_404(id_factura)
            id_reporteMensual = factura.id_reporteMensual  # Capturar el ID del reporte antes de eliminar
            db.session.delete(factura)
            db.session.commit()

            # Llamar al Stored Procedure para actualizar el reporte mensual
            if id_reporteMensual:
                stored_proc = text("EXEC sp_UpdateReporteMensual :id")
                db.session.execute(stored_proc, {'id': id_reporteMensual})
                db.session.commit()

            return '', 204
        except Exception as e:
            abort(400, message=f"Error al eliminar la factura: {str(e)}")
