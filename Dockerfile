# Usar la imagen oficial ligera de Python
FROM python:3.11-slim

# Establecer directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto por el que correrá FastAPI
EXPOSE 8000

# Comando para arrancar el servidor en producción con uvicorn (sin reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
