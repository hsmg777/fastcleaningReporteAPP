from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from controllers.Orden import blp as OrdenBluePrint
from controllers.Gastos import blp as GastosBluePrint
from controllers.ReporteMensual import blp as ReporteMensualBluePrint
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
    server = '(localdb)\\MSSQLLocalDB'
    database = 'FastCleaning'
    username = 'aurora'
    password = 'mamifer1'
    driver = 'ODBC Driver 17 for SQL Server'
        
    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
