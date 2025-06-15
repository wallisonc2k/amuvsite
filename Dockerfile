# ---------- Stage 1: Build do Tailwind CSS ----------
FROM node:20 AS frontend

# Definindo diretório de trabalho
WORKDIR /app

# Copiando apenas o necessário para instalar o Node e o Tailwind
COPY package.json package-lock.json ./
COPY tailwind.config.js postcss.config.js ./

# Instalando dependências do frontend
RUN npm ci

# Copiando todo o projeto para que o Tailwind processe seus templates e CSS
COPY . .

# Gerando o CSS final (output em static/)
RUN npm run build:css


# ---------- Stage 2: Build da aplicação Django ----------
FROM python:3.11-slim AS backend

# Variáveis de ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependências de SO necessárias (PostgreSQL client etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar dependências Python e instalar
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código da aplicação
COPY . .

# Copiar o CSS compilado pelo Tailwind da primeira stage
COPY --from=frontend /app/static/shared/css/output.css /app/static/shared/css/output.css

# Coletar arquivos estáticos do Django
RUN python manage.py collectstatic --noinput

# Expor a porta para Cloud Run (ou qualquer orquestrador)
EXPOSE 8080

# Comando padrão para iniciar o Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "amuvsite.wsgi:application"]
