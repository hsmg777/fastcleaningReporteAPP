"""Añadir stored procedure sp_UpdateReporteMensual

Revision ID: dcbaf1f48031
Revises: bc88dd8642b6
Create Date: 2025-03-08 15:17:42.062817

"""
from alembic import op
import sqlalchemy as sa


# Identificadores de la migración
revision = 'dcbaf1f48031'
down_revision = 'bc88dd8642b6'
branch_labels = None
depends_on = None


def upgrade():
    # Eliminar el procedimiento si ya existe
    op.execute("DROP PROCEDURE IF EXISTS sp_UpdateReporteMensual;")

    # Crear el Stored Procedure sin usar DELIMITER
    op.execute("""
        CREATE PROCEDURE sp_UpdateReporteMensual(IN reporte_id INT)
        BEGIN
            -- Actualizar total neto sumando los valores de la tabla Orden
            UPDATE ReporteMensual
            SET totalNeto = (
                SELECT IFNULL(SUM(valor), 0) 
                FROM Orden 
                WHERE id_reporteMensual = reporte_id
            )
            WHERE id_reporteMensual = reporte_id;

            -- Actualizar total de gastos sumando los valores de la tabla Gastos
            UPDATE ReporteMensual
            SET totalGastos = (
                SELECT IFNULL(SUM(valor), 0) 
                FROM Gastos 
                WHERE id_reporteMensual = reporte_id
            )
            WHERE id_reporteMensual = reporte_id;

            -- Calcular la ganancia como totalNeto - totalGastos
            UPDATE ReporteMensual
            SET ganancia = totalNeto - totalGastos
            WHERE id_reporteMensual = reporte_id;
        END;
    """)


def downgrade():
    # Eliminar el Stored Procedure si se hace un rollback
    op.execute("DROP PROCEDURE IF EXISTS sp_UpdateReporteMensual;")
