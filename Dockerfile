# Usa una imagen base de Python
FROM python:3.11-slim

# Actualiza e instala dependencias necesarias para ODBC y pyodbc
RUN apt-get update && apt-get install -y \
    curl gnupg apt-transport-https unixodbc-dev \
    build-essential pkg-config libssl-dev libffi-dev libmariadb-dev-compat libmariadb-dev \
    gcc g++ python3-dev unixodbc && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean

# Configura el directorio de trabajo
WORKDIR /app

# Copia el contenido del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expon el puerto 5000
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
