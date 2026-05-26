# Usar imagen oficial de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto del backend solicitado en el proyecto
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"]