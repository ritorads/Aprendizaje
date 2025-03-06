# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Exponer el puerto que utilizará la app (por defecto, Railway suele usar el puerto 8080)
EXPOSE 8080

# Establece la variable de entorno para producción
ENV FLASK_ENV=production

# Ejecuta la aplicación usando gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]
