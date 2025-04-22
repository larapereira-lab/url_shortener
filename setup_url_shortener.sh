#!/bin/bash

set -e

PROJETO_DIR="$HOME/projetos/url_shortener"
COMPARTILHADA_DIR="$HOME/compartilhada"

echo "✅ Iniciando setup do projeto URL Shortener..."

# Verifica se o diretório do projeto existe
mkdir -p "$PROJETO_DIR"

echo "📁 Copiando arquivos da pasta compartilhada..."
cp -r "$COMPARTILHADA_DIR"/app "$PROJETO_DIR" 2>/dev/null || echo "⚠️ Pasta 'app' já existe ou não foi encontrada."

if [ -f "$COMPARTILHADA_DIR/docker-compose.yml" ]; then
    cp "$COMPARTILHADA_DIR/docker-compose.yml" "$PROJETO_DIR"
else
    echo "❌ docker-compose.yml não encontrado em $COMPARTILHADA_DIR"
    exit 1
fi

# Verificação extra do requirements.txt
if [ ! -f "$PROJETO_DIR/app/requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado em $PROJETO_DIR/app"
    exit 1
fi

cd "$PROJETO_DIR"

echo "🐳 Subindo o container..."
docker compose up --build

