# Imagen base ligera con Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la app
COPY app/ .



# Expone el puerto donde se ejecuta FastAPI
EXPOSE 3030

# Comando para lanzar el servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3030"]