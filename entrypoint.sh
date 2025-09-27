#!/bin/bash
set -e

if [ "$INIT_DB" = "true" ]; then
    echo ">> Inicializando base de datos con schema y data..."
else
    echo ">> Saltando inicialización de datos..."
    rm -rf /docker-entrypoint-initdb.d/1_data.sql
fi

exec docker-entrypoint.sh "$@"
