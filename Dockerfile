# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala Flask y Flask-RESTX directamente
RUN pip install --no-cache-dir flask flask-restx numpy

# Copia todos los archivos de tu proyecto al contenedor
COPY . .

# Expone el puerto 8080
EXPOSE 8080

# Comando para arrancar la aplicación
CMD ["python", "Ejercicio 1 SW.py"]