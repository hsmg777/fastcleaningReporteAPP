#!/bin/bash

# Actualizar los paquetes
apt-get update

# Instalar dependencias para el controlador ODBC
apt-get install -y curl gnupg apt-transport-https

# Agregar la clave y el repositorio de Microsoft para ODBC
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualizar los paquetes nuevamente
apt-get update

# Instalar el controlador ODBC
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
