from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models.ReporteMensual import ReporteMensual
from schemas.ReporteMensualSchema import ReporteMensualSchema

# Crear el Blueprint
blp = Blueprint("ReporteMensual", __name__, url_prefix="/tasks/reportes", description="Operaciones CRUD para Reportes Mensuales")

# Schemas
reporte_schema = ReporteMensualSchema()
reportes_schema = ReporteMensualSchema(many=True)


# Rutas para /tasks/reportes
@blp.route('/')
class ReporteMensualList(MethodView):
    @blp.response(200, ReporteMensualSchema(many=True))  # Define el esquema para la respuesta
    def get(self):
        """Obtener todos los reportes mensuales"""
        reportes = ReporteMensual.query.all()
        return reportes

    @blp.arguments(ReporteMensualSchema)  # Valida la entrada con el esquema
    @blp.response(201, ReporteMensualSchema)  # Define el esquema para la respuesta
    def post(self, data):
        """Crear un nuevo reporte mensual"""
        try:
            nuevo_reporte = ReporteMensual(
                nombreMes=data['nombreMes']
            )
            db.session.add(nuevo_reporte)
            db.session.commit()
            return nuevo_reporte
        except Exception as e:
            abort(400, message=f"Error al crear el reporte mensual: {str(e)}")


# Rutas para /tasks/reportes/<int:id_reporteMensual>
@blp.route('/<int:id_reporteMensual>')
class ReporteMensualResource(MethodView):
    @blp.response(200, ReporteMensualSchema)  # Define el esquema para la respuesta
    def get(self, id_reporteMensual):
        """Obtener un reporte mensual por su ID"""
        reporte = ReporteMensual.query.get_or_404(id_reporteMensual)
        return reporte

    @blp.arguments(ReporteMensualSchema)  # Valida la entrada con el esquema
    @blp.response(200, ReporteMensualSchema)  # Define el esquema para la respuesta
    def put(self, data, id_reporteMensual):
        """Actualizar un reporte mensual existente"""
        reporte = ReporteMensual.query.get_or_404(id_reporteMensual)
        if 'nombreMes' in data:
            reporte.nombreMes = data['nombreMes']
        db.session.commit()
        return reporte

    @blp.response(204)  # Sin contenido en la respuesta
    def delete(self, id_reporteMensual):
        """Eliminar un reporte mensual"""
        reporte = ReporteMensual.query.get_or_404(id_reporteMensual)
        db.session.delete(reporte)
        db.session.commit()
        return '', 204
