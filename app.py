from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_migrate import Migrate
from db import db, init_db
from dotenv import load_dotenv
import os

from controllers.Orden import blp as OrdenBluePrint
from controllers.Gastos import blp as GastosBluePrint
from controllers.ReporteMensual import blp as ReporteMensualBluePrint
from controllers.Factura import blp as FacturaBluePrint

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración de la API requerida por flask_smorest
    app.config["API_TITLE"] = "ReporteFC API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configuración de la base de datos
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_driver = os.getenv("DB_DRIVER", "mysql")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)
    api = Api(app)

    api.register_blueprint(OrdenBluePrint)
    api.register_blueprint(GastosBluePrint)
    api.register_blueprint(ReporteMensualBluePrint)
    api.register_blueprint(FacturaBluePrint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
