# Image untuk server online (Render, Koyeb, Fly.io, Hugging Face Spaces, dll.)
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    FLET_FORCE_WEB_SERVER=true \
    PORT=8550
WORKDIR /app
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt
COPY . .
EXPOSE 8550
CMD ["python", "main.py"]
