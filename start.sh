#!/bin/bash

# Ejecuta tu aplicación Flask
gunicorn -w 4 -b 0.0.0.0:5000 app:app
