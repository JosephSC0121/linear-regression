# Usa una imagen base de Python y Spark
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Define el comando para ejecutar tu aplicación
CMD ["python", "process.py"]
