# Usa una imagen base de Python
FROM python:3.11-slim

# Instala dependencias necesarias para MySQL y Flask
RUN apt-get update && apt-get install -y \
    curl gnupg apt-transport-https unixodbc-dev \
    build-essential pkg-config libssl-dev libffi-dev libmariadb-dev-compat libmariadb-dev \
    gcc g++ python3-dev unixodbc && \
    apt-get clean

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Verifica que Flask-Migrate está instalado
RUN pip show flask-migrate

# Expon el puerto 5000
EXPOSE 5000

# Ejecuta migraciones antes de iniciar la aplicación
CMD ["sh", "-c", "flask db upgrade && gunicorn --workers=4 --bind 0.0.0.0:5000 'app:create_app()'"]
