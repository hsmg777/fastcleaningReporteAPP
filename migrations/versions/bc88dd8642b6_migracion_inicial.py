"""Migración inicial

Revision ID: bc88dd8642b6
Revises: 
Create Date: 2025-03-08 13:37:03.055751

"""
from alembic import op
import sqlalchemy as sa


# Identificadores de la migración
revision = 'bc88dd8642b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla ReporteMensual (Debe ir primero porque otras tablas la referencian)
    op.create_table(
        'ReporteMensual',
        sa.Column('id_reporteMensual', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombreMes', sa.String(length=50), nullable=False),
        sa.Column('totalNeto', sa.Float(), nullable=False, server_default="0.0"),
        sa.Column('totalGastos', sa.Float(), nullable=False, server_default="0.0"),
        sa.Column('ganancia', sa.Float(), nullable=False, server_default="0.0"),
        sa.PrimaryKeyConstraint('id_reporteMensual')
    )

    # Crear tabla Factura
    op.create_table(
        'Factura',
        sa.Column('id_factura', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('numeroFactura', sa.Integer(), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False, default=sa.func.current_date()),
        sa.Column('id_reporteMensual', sa.Integer(), sa.ForeignKey('ReporteMensual.id_reporteMensual', ondelete="SET NULL"), nullable=True),
        sa.PrimaryKeyConstraint('id_factura')
    )

    # Crear tabla Gastos
    op.create_table(
        'Gastos',
        sa.Column('id_gastos', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombreGasto', sa.String(length=50), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False, default=sa.func.current_date()),
        sa.Column('id_reporteMensual', sa.Integer(), sa.ForeignKey('ReporteMensual.id_reporteMensual', ondelete="SET NULL"), nullable=True),
        sa.PrimaryKeyConstraint('id_gastos')
    )

    # Crear tabla Orden
    op.create_table(
        'Orden',
        sa.Column('id_orden', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('numeroOrden', sa.Integer(), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False, default=sa.func.current_date()),
        sa.Column('id_reporteMensual', sa.Integer(), sa.ForeignKey('ReporteMensual.id_reporteMensual', ondelete="SET NULL"), nullable=True),
        sa.PrimaryKeyConstraint('id_orden')
    )


def downgrade():
    # Eliminar tablas en orden inverso para evitar problemas de claves foráneas
    op.drop_table('Orden')
    op.drop_table('Gastos')
    op.drop_table('Factura')
    op.drop_table('ReporteMensual')
