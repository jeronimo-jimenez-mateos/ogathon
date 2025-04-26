# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos de tu proyecto al contenedor
COPY ./src /app

# Instala Flask y Flask-RESTX directamente
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto 8080
EXPOSE 8080

# Comando para arrancar ambos scripts
CMD ["python", "Ejercicio 1 SW.py"]