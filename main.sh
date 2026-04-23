#!/bin/bash
# Get directory where is this file located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Buscando en: $SCRIPT_DIR"
ls -la "$SCRIPT_DIR"

LOCKFILE="$SCRIPT_DIR/sync.lock"

# Verifca que exista el lock file
echo "Buscando $LOCKFILE"
if [ -f $LOCKFILE ]; then
    echo "Lock file encontrado, abortando tranmission"
    exit;
fi

echo "Iniciando copia"
touch $LOCKFILE

# Load .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Cargando variables de entorno"
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
else
    echo "Error crítico: No se encontró el archivo .env en $SCRIPT_DIR"
    exit 1
fi

# Python sincroniza y organiza
python3 $SCRIPT_DIR/main.py

rm "$LOCKFILE"
