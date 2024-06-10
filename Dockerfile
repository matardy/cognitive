FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Node.js y npm
RUN apt-get update && apt-get install -y nodejs npm

# Copiar archivos de configuración antes para aprovechar la caché de Docker
COPY requirements.txt .
COPY package*.json ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Instalar dependencias de npm
RUN npm install

# Copiar el resto de la aplicación al contenedor
COPY . .

# Establecer PYTHONPATH para incluir el directorio /app
ENV PYTHONPATH=/app/app

# Ejecutar las migraciones de Alembic antes de iniciar la aplicación
RUN alembic upgrade head

# Copia el script de entrada y configúralo como el punto de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
