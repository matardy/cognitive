FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia el resto de tu aplicación y la configuración de Alembic al contenedor
COPY . .

# Establecer PYTHONPATH para incluir el directorio /app
ENV PYTHONPATH=/app/app

# Copia el script de entrada y configúralo como el punto de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
