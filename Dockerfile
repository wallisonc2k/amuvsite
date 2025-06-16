# ----------------------------------------------------------------------
# Stage 1: Build do Frontend (Tailwind CSS)
# Este estágio usa Node.js para compilar os assets de CSS.
# ----------------------------------------------------------------------
FROM node:20 AS frontend

WORKDIR /app

# Copia apenas o necessário para instalar as dependências, aproveitando o cache do Docker
COPY package.json package-lock.json ./
COPY tailwind.config.js postcss.config.js ./

# Instala as dependências do frontend de forma otimizada
RUN npm ci

# Copia o resto do código fonte para que o Tailwind possa escanear os templates
COPY . .

# Executa o build do CSS
RUN npm run build:css


# ----------------------------------------------------------------------
# Stage 2: Builder do Backend (Python/Django)
# Este estágio instala dependências, prepara o ambiente e coleta os arquivos estáticos.
# Ele contém ferramentas de build que não irão para a imagem final.
# ----------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Variáveis de ambiente para otimizar o Python em contêineres
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do sistema operacional necessárias para compilar pacotes Python (ex: psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria um usuário e grupo 'app' não-root para rodar a aplicação com segurança
RUN addgroup --system app && adduser --system --group app

# Define o diretório de trabalho
WORKDIR /app

# Cria um ambiente virtual para isolar as dependências Python
RUN python -m venv /opt/venv
# Adiciona o venv ao PATH do sistema
ENV PATH="/opt/venv/bin:$PATH"

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .
# Instala as dependências Python dentro do ambiente virtual
RUN pip install -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Copia o CSS compilado do estágio do frontend para o diretório de estáticos da aplicação
COPY --from=frontend /app/static/shared/css/output.css /app/static/shared/css/output.css

# Coleta todos os arquivos estáticos do Django.
# - DJANGO_ENV=production: Garante que as settings de produção sejam carregadas.
# - DJANGO_SECRET_KEY: Fornece uma chave dummy, pois é necessária para o comando. Use o nome da variável do seu settings.py.
# - DATABASE_URL: (Opcional, mas recomendado) Força o uso de um banco em memória para evitar erros de conexão com o Postgres durante o build.
#   Para isto funcionar, instale 'dj-database-url' e use-o no seu settings.py.
RUN DJANGO_ENV="production" \
    DJANGO_SECRET_KEY="dummy-key-for-build-dont-use-in-prod" \
    python manage.py collectstatic --noinput

# Muda a propriedade de todos os arquivos para o usuário 'app'
RUN chown -R app:app /app /opt/venv


# ----------------------------------------------------------------------
# Stage 3: Imagem Final (Runtime)
# Este é o estágio final. Ele cria a imagem mais leve e segura possível,
# contendo apenas o necessário para rodar a aplicação.
# ----------------------------------------------------------------------
FROM python:3.11-slim AS final

# Instala apenas as dependências de sistema operacional para RUNTIME (ex: cliente do Postgres)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Cria o mesmo usuário e grupo 'app'
RUN addgroup --system app && adduser --system --group app

# Define o diretório de trabalho
WORKDIR /app

# Copia o ambiente virtual com as dependências já instaladas do estágio 'builder'
COPY --from=builder --chown=app:app /opt/venv /opt/venv

# Copia o código da aplicação (que agora inclui os estáticos coletados) do estágio 'builder'
COPY --from=builder --chown=app:app /app /app

# Adiciona o venv ao PATH do sistema
ENV PATH="/opt/venv/bin:$PATH"

# Define 'app' como o usuário que irá rodar o processo. Mais seguro que 'root'.
USER app

# Expõe a porta que o Gunicorn irá usar
EXPOSE 8080

# Comando para iniciar a aplicação em produção com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "amuvsite.wsgi:application"]