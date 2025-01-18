from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from controllers.Orden import blp as OrdenBluePrint
from controllers.Gastos import blp as GastosBluePrint
from controllers.ReporteMensual import blp as ReporteMensualBluePrint
from controllers.Factura import blp as FacturaBluePrint
from db import init_db
import urllib.parse

def create_app(testing=False):
    app = Flask(__name__)
    
    # Configuración general
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ReporteFC API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configuración de la conexión a la base de datos
    server = 'ingwebserver.database.windows.net'
    database = 'FastCleaning'
    username = 'aurora'
    password = 'Mamifer_1'
    driver = 'ODBC Driver 17 for SQL Server'

    # Codificar los parámetros de conexión
    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    
    # Crear la cadena de conexión para SQLAlchemy
    connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos
    init_db(app)

    # Habilitar CORS
    CORS(app)

    # Inicializar API
    api = Api(app)

    # Registrar el Blueprint
    api.register_blueprint(OrdenBluePrint)
    api.register_blueprint(GastosBluePrint)
    api.register_blueprint(ReporteMensualBluePrint)
    api.register_blueprint(FacturaBluePrint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
